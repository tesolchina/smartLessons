# File Migration Summary - LANG2077 to Canva Automation

**Date:** September 6, 2025  
**Migration:** LANG2077 Canva-related files moved to centralized automation folder

## Files Moved

### From: `/projects/LANG2077/`
### To: `/operating/canva_automation/`

**Main Scripts:**
- `canva_slide_creator.py` → `canva_slide_creator.py` 
- `CANVA_CLI_SETUP_GUIDE.md` → `CANVA_CLI_SETUP_GUIDE.md`

### To: `/operating/canva_automation/lang2077_materials/`

**Course Materials:**
- `presentation_materials/canva_creation_guide.md` → `lang2077_materials/canva_creation_guide.md`
- `presentation_materials/lang2077_slides_content.md` → `lang2077_materials/lang2077_slides_content.md`
- `presentation_materials/lang2077_slides_data.json` → `lang2077_materials/lang2077_slides_data.json`
- `presentation_materials/powerpoint_creation_guide.md` → `lang2077_materials/powerpoint_creation_guide.md`
- `requirements.txt` → `lang2077_materials/requirements_original.txt` (renamed to avoid conflict)

## Remaining in LANG2077 Project

**Course-specific content (non-Canva):**
- `CourseDocs/` - Course documentation
- `LANG2077_Slides_Outline.md` - Slide content outline
- `notesUpdate.md` - Course notes
- Service learning email files (4 files)

## Benefits of Migration

1. **Centralized Automation:** All Canva scripts are now in one location
2. **Reusability:** Scripts can be used for other courses and projects
3. **Better Organization:** Course content separated from automation tools
4. **Collaboration:** Enhanced collaboration tools are co-located

## Updated File Paths

**For LANG2077 course materials:**
- Slide content: `/operating/canva_automation/lang2077_materials/lang2077_slides_content.md`
- Creation guides: `/operating/canva_automation/lang2077_materials/canva_creation_guide.md`
- Structured data: `/operating/canva_automation/lang2077_materials/lang2077_slides_data.json`

**For Canva automation tools:**
- Main CLI: `/operating/canva_automation/canva_cli.py`
- Collaborative CLI: `/operating/canva_automation/canva_collaborative_cli.py`
- Helper tools: `/operating/canva_automation/canva_collaboration_helper.py`
- Quick commands: `/operating/canva_automation/canva_commands.sh`

## Next Steps

1. Update any scripts that reference the old paths
2. Test the moved scripts in their new location
3. Update documentation to reflect new file structure
4. Consider creating symbolic links if needed for backward compatibility
