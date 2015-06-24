import sys
if (sys.version_info > (3, 0)):
    from .dmp_py3 import diff_match_patch, patch_obj
else:
    from .dmp_py2 import diff_match_patch, patch_obj
