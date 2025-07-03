from typing import Any, List

from fastapi import logger as fastapi_logger

from apps.modules.quinn.slides.schemas.survey_data_analysis_schema import Slide

logger = fastapi_logger.logger


def find_layout_and_placeholders_for_new_structure(  # noqa: C901, PLR0912, PLR0915
    available_layouts: list[dict[str, Any]],
    slide_data_item: dict[str, Any],
) -> tuple[str | None, dict[str, Any]]:
    """Find the layout and placeholders for a new structure."""

    slide_type = slide_data_item.get("slide_type")
    has_title = bool(slide_data_item.get("title"))
    has_bullets = slide_type in ["Background", "Image Left", "Image Right"] and bool(
        slide_data_item.get("bullet_points"),
    )
    has_description = slide_type in [
        "Background",
        "Image Left",
        "Image Right",
    ] and bool(
        slide_data_item.get("description"),
    )
    has_image = slide_type in ["Image Left", "Image Right"] and bool(
        slide_data_item.get("image_url"),
    )

    chosen_layout_object = None
    for layout_obj in available_layouts:
        if layout_obj.get("layoutProperties", {}).get("displayName") == slide_type:
            chosen_layout_object = layout_obj
            break

    if not chosen_layout_object:
        logger.error("Error: No layouts available in 'available_layouts'.")
        return None, {}

    best_layout_id = chosen_layout_object.get("objectId")
    best_placeholder_map = {}

    placeholders_on_chosen_layout: dict[str, dict[int, str]] = {}
    for pe in chosen_layout_object.get("pageElements", []):
        if pe.get("shape") and pe["shape"].get("placeholder"):
            ph = pe["shape"]["placeholder"]
            ph_type = ph.get("type")
            ph_idx = ph.get("index", 0)
            ph_obj_id = pe.get("objectId")

            if ph_type not in placeholders_on_chosen_layout:
                placeholders_on_chosen_layout[ph_type] = {}
            placeholders_on_chosen_layout[ph_type][ph_idx] = ph_obj_id
        elif (
            pe.get("image")
            and pe.get("image").get("placeholder", {}).get("type") == "PICTURE"
        ):
            if "PICTURE" not in placeholders_on_chosen_layout:
                placeholders_on_chosen_layout["PICTURE"] = {}
            placeholders_on_chosen_layout["PICTURE"][0] = pe.get("objectId")

    if has_title:
        if (
            "TITLE" in placeholders_on_chosen_layout
            and 0 in placeholders_on_chosen_layout["TITLE"]
        ):
            best_placeholder_map["TITLE"] = placeholders_on_chosen_layout["TITLE"][0]
        elif (
            "CENTERED_TITLE" in placeholders_on_chosen_layout
            and 0 in placeholders_on_chosen_layout["CENTERED_TITLE"]
        ):
            best_placeholder_map["TITLE"] = placeholders_on_chosen_layout[
                "CENTERED_TITLE"
            ][0]
        elif (
            "SUBTITLE" in placeholders_on_chosen_layout
            and 0 in placeholders_on_chosen_layout["SUBTITLE"]
        ):
            best_placeholder_map["TITLE"] = placeholders_on_chosen_layout["SUBTITLE"][0]

    if has_image and "PICTURE" in placeholders_on_chosen_layout:
        if 0 in placeholders_on_chosen_layout["PICTURE"]:
            best_placeholder_map["IMAGE"] = placeholders_on_chosen_layout["PICTURE"][0]
        else:
            for pic_idx in sorted(placeholders_on_chosen_layout["PICTURE"].keys()):
                best_placeholder_map["IMAGE"] = placeholders_on_chosen_layout[
                    "PICTURE"
                ][pic_idx]
                break

    body_ph_ids_available = []
    if "BODY" in placeholders_on_chosen_layout:
        for idx in sorted(placeholders_on_chosen_layout["BODY"].keys()):
            body_ph_ids_available.append(placeholders_on_chosen_layout["BODY"][idx])

    subtitle_ph_ids_available = []
    if "SUBTITLE" in placeholders_on_chosen_layout:
        for idx in sorted(placeholders_on_chosen_layout["SUBTITLE"].keys()):
            if placeholders_on_chosen_layout["SUBTITLE"][
                idx
            ] != best_placeholder_map.get("TITLE"):
                subtitle_ph_ids_available.append(
                    placeholders_on_chosen_layout["SUBTITLE"][idx],
                )

    if has_bullets and body_ph_ids_available:
        best_placeholder_map["BULLETS"] = body_ph_ids_available.pop(
            0,
        )  # Take the first available BODY

    if has_description:
        if body_ph_ids_available:
            best_placeholder_map["DESCRIPTION"] = body_ph_ids_available.pop(0)
        elif subtitle_ph_ids_available:
            best_placeholder_map["DESCRIPTION"] = subtitle_ph_ids_available.pop(0)

    if has_title and "TITLE" not in best_placeholder_map:
        logger.warning(
            f"Warning: Title expected but no 'TITLE', 'CENTERED_TITLE', or 'SUBTITLE' placeholder mapped for layout {best_layout_id}.",
        )
    if has_bullets and "BULLETS" not in best_placeholder_map:
        logger.warning(
            f"Warning: Bullet points expected for slide_type '{slide_type}' but no 'BODY' placeholder mapped for 'BULLETS' on layout {best_layout_id}.",
        )
    if has_description and "DESCRIPTION" not in best_placeholder_map:
        logger.warning(
            f"Warning: Description expected for slide_type '{slide_type}' but no ('BODY' or 'SUBTITLE') placeholder mapped for 'DESCRIPTION' on layout {best_layout_id}.",
        )
    if has_image and "IMAGE" not in best_placeholder_map:
        logger.warning(
            f"Warning: Image expected but no 'PICTURE' placeholder mapped for 'IMAGE' on layout {best_layout_id}.",
        )

    return best_layout_id, best_placeholder_map


def create_google_slides_presentation(  # noqa: C901
    slides_json_data: List[Slide],
    presentation_id: str,
    available_layouts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create a Google Slides presentation from a list of slides."""

    logger.info(f"Preparing requests for presentation ID: {presentation_id}")
    requests = []

    for i, slide_data_model in enumerate(slides_json_data):
        slide_data = slide_data_model.model_dump()
        slide_object_id = f"slide_{i}"
        slide_type = slide_data.get("slide_type")

        title_element_id = f"title_element_{i}"
        bullets_element_id = f"bullets_element_{i}"
        description_element_id = f"description_element_{i}"
        image_element_id = f"image_element_{i}"

        chosen_layout_id, master_placeholders = (
            find_layout_and_placeholders_for_new_structure(
                available_layouts,
                slide_data,
            )
        )

        if not chosen_layout_id:
            logger.error(
                f"Error: Slide {i} - Could not assign a layoutId. Skipping slide.",
            )
            continue

        logger.info(
            f"Slide {i} ({slide_type}): Using layoutId '{chosen_layout_id}'. Master placeholders found: {master_placeholders}",
        )

        create_slide_params: dict[str, Any] = {
            "objectId": slide_object_id,
            "slideLayoutReference": {"layoutId": chosen_layout_id},
            "placeholderIdMappings": [],
        }

        if slide_data.get("title") and master_placeholders.get("TITLE"):
            create_slide_params["placeholderIdMappings"].append(
                {
                    "layoutPlaceholderObjectId": master_placeholders["TITLE"],
                    "objectId": title_element_id,
                },
            )

        if (
            slide_type in ["Background", "Image Left", "Image Right"]
            and slide_data.get("bullet_points")
            and master_placeholders.get("BULLETS")
        ):
            create_slide_params["placeholderIdMappings"].append(
                {
                    "layoutPlaceholderObjectId": master_placeholders["BULLETS"],
                    "objectId": bullets_element_id,
                },
            )

        if (
            slide_type in ["Background", "Image Left", "Image Right"]
            and slide_data.get("description")
            and master_placeholders.get("DESCRIPTION")
        ):
            create_slide_params["placeholderIdMappings"].append(
                {
                    "layoutPlaceholderObjectId": master_placeholders["DESCRIPTION"],
                    "objectId": description_element_id,
                },
            )

        if (
            slide_type in ["Image Left", "Image Right"]
            and slide_data.get("image_url")
            and master_placeholders.get("IMAGE")
        ):
            create_slide_params["placeholderIdMappings"].append(
                {
                    "layoutPlaceholderObjectId": master_placeholders["IMAGE"],
                    "objectId": image_element_id,
                },
            )

        requests.append({"createSlide": create_slide_params})

        if slide_data.get("title") and master_placeholders.get("TITLE"):
            requests.append(
                {
                    "insertText": {
                        "objectId": title_element_id,
                        "text": slide_data["title"],
                        "insertionIndex": 0,
                    },
                },
            )

        if (
            slide_type in ["Background", "Image Left", "Image Right"]
            and slide_data.get("bullet_points")
            and master_placeholders.get("BULLETS")
        ):
            bullet_text = "\n".join(slide_data["bullet_points"])
            if bullet_text:
                requests.append(
                    {
                        "insertText": {
                            "objectId": bullets_element_id,
                            "text": bullet_text,
                            "insertionIndex": 0,
                        },
                    },
                )
                requests.append(
                    {
                        "createParagraphBullets": {
                            "objectId": bullets_element_id,
                            "textRange": {"type": "ALL"},
                            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                        },
                    },
                )

        if (
            slide_type in ["Background", "Image Left", "Image Right"]
            and slide_data.get("description")
            and master_placeholders.get("DESCRIPTION")
        ):
            requests.append(
                {
                    "insertText": {
                        "objectId": description_element_id,
                        "text": slide_data["description"],
                        "insertionIndex": 0,
                    },
                },
            )

        if (
            slide_type in ["Image Left", "Image Right"]
            and slide_data.get("image_url")
            and master_placeholders.get("IMAGE")
        ):
            requests.append(
                {
                    "replaceImage": {
                        "imageObjectId": image_element_id,
                        "url": slide_data["image_url"],
                        "imageReplaceMethod": "CENTER_INSIDE",
                    },
                },
            )

    return requests
