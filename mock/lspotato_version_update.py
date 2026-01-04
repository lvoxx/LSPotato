"""
Mock Update Data for Testing UI
================================
This file provides fake update data for testing the update UI without actually
calling GitHub API. Comment out the import in utils.py when going to production.

Usage in utils.py:
    # FOR TESTING ONLY - Comment out in production
    from .mock_update_data import get_mock_update_data
    return get_mock_update_data()  # Replace actual API call
"""

from ..utils.logger import get_logger

logger = get_logger("UpdateChecker.Mock")


def get_mock_update_data():
    """
    Returns mock update data for testing
    
    Test scenarios available:
    - SCENARIO_NO_UPDATE: Already on latest version
    - SCENARIO_PATCH_ONLY: Only patch update available (1.0.18 -> 1.0.20)
    - SCENARIO_MINOR_ONLY: Only minor update available (1.0.18 -> 1.1.1)
    - SCENARIO_BOTH: Both patch and minor available (1.0.18 -> 1.0.20 + 1.1.1)
    - SCENARIO_MAJOR: Major version update (1.0.18 -> 2.0.0)
    
    Change ACTIVE_SCENARIO to test different cases
    """
    
    # ============================================
    # CHANGE THIS TO TEST DIFFERENT SCENARIOS
    # ============================================
    ACTIVE_SCENARIO = "SCENARIO_BOTH"  # Options: NO_UPDATE, PATCH_ONLY, MINOR_ONLY, BOTH, MAJOR
    
    
    # Assume current version is (1, 0, 18)
    current_version = (1, 0, 18)
    
    scenarios = {
        "SCENARIO_NO_UPDATE": {
            'has_update': False,
            'current_version': current_version,
            'latest_tag': "v1.0.18",
            'branch_update': None,
            'major_update': None,
            'description': "Already on latest version"
        },
        
        "SCENARIO_PATCH_ONLY": {
            'has_update': True,
            'current_version': current_version,
            'latest_tag': "v1.0.20",
            'branch_update': "v1.0.20",  # Patch update in same branch
            'major_update': None,
            'description': "Patch update available: 1.0.18 -> 1.0.20"
        },
        
        "SCENARIO_MINOR_ONLY": {
            'has_update': True,
            'current_version': current_version,
            'latest_tag': "v1.1.1",
            'branch_update': "v1.1.1",  # Next minor version
            'major_update': None,
            'description': "Minor update available: 1.0.18 -> 1.1.1"
        },
        
        "SCENARIO_BOTH": {
            'has_update': True,
            'current_version': current_version,
            'latest_tag': "v1.1.1",  # Latest overall
            'branch_update': "v1.0.20",  # Safe patch update
            'major_update': "v1.1.1",   # Minor version (treated as major for decision)
            'description': "Multiple updates available: 1.0.20 (safe) or 1.1.1 (new features)"
        },
        
        "SCENARIO_MAJOR": {
            'has_update': True,
            'current_version': current_version,
            'latest_tag': "v2.0.0",
            'branch_update': None,
            'major_update': "v2.0.0",  # Major version jump
            'description': "Major update available: 1.0.18 -> 2.0.0"
        },
        
        # Extra scenarios for comprehensive testing
        "SCENARIO_SKIP_MINOR": {
            'has_update': True,
            'current_version': current_version,
            'latest_tag': "v1.2.0",
            'branch_update': None,
            'major_update': "v1.2.0",  # Skips 1.1.x branch
            'description': "Skipped minor version: 1.0.18 -> 1.2.0 (treated as major)"
        },
    }
    
    if ACTIVE_SCENARIO not in scenarios:
        logger.warning(f"Unknown scenario: {ACTIVE_SCENARIO}, defaulting to NO_UPDATE")
        ACTIVE_SCENARIO = "SCENARIO_NO_UPDATE"
    
    mock_data = scenarios[ACTIVE_SCENARIO]
    
    # Log the mock scenario being used
    logger.info("=" * 60)
    logger.info("🎭 MOCK UPDATE DATA ACTIVE")
    logger.info(f"Scenario: {ACTIVE_SCENARIO}")
    logger.info(f"Description: {mock_data['description']}")
    logger.info(f"Current: {mock_data['current_version']}")
    logger.info(f"Latest: {mock_data['latest_tag']}")
    logger.info(f"Branch Update: {mock_data['branch_update']}")
    logger.info(f"Major Update: {mock_data['major_update']}")
    logger.info("=" * 60)
    
    return mock_data


# ============================================
# DETAILED MOCK SCENARIOS DOCUMENTATION
# ============================================

"""
TESTING GUIDE:
==============

1. SCENARIO_NO_UPDATE
   - Tests: "Already on latest" message
   - Expected UI: Simple info message, no update buttons
   - Use case: User has latest version

2. SCENARIO_PATCH_ONLY
   - Tests: Simple notification popup for patch updates
   - Expected UI: Single update button to v1.0.20 with "Safe to update" message
   - Use case: Bug fix release

3. SCENARIO_MINOR_ONLY
   - Tests: Simple notification popup for minor updates
   - Expected UI: Single update button to v1.1.1 with "New features" message
   - Use case: Next minor version with new features

4. SCENARIO_BOTH (MOST IMPORTANT)
   - Tests: Decision popup with two options
   - Expected UI: 
     * Option 1: Update to v1.0.20 (Recommended, safe)
     * Option 2: Update to v1.1.1 (Advanced, new features)
   - Use case: Give user choice between stability and features

5. SCENARIO_MAJOR
   - Tests: Major update warning popup + confirmation
   - Expected UI: 
     * Red warning about major changes
     * Backup reminder
     * Confirmation dialog before proceeding
   - Use case: Breaking changes, new major version

6. SCENARIO_SKIP_MINOR
   - Tests: Skipped version handling (1.0.x -> 1.2.x)
   - Expected UI: Treated as major update with warnings
   - Use case: User skipped an entire minor version branch

QUICK TEST CHECKLIST:
=====================
[ ] Test each scenario individually
[ ] Verify popup appearance and layout
[ ] Check button colors (red for risky actions)
[ ] Verify version numbers displayed correctly
[ ] Test "Not Now" button functionality
[ ] Test actual update button (mock download?)
[ ] Verify logging output in console
"""


def get_mock_release_list():
    """
    Returns a mock list of all available releases
    Useful for testing release selection UI
    """
    return [
        {"tag_name": "v2.0.0", "name": "Version 2.0.0 - Major Release"},
        {"tag_name": "v1.2.0", "name": "Version 1.2.0 - Feature Update"},
        {"tag_name": "v1.1.1", "name": "Version 1.1.1 - Minor Update"},
        {"tag_name": "v1.1.0", "name": "Version 1.1.0 - New Features"},
        {"tag_name": "v1.0.20", "name": "Version 1.0.20 - Bug Fixes"},
        {"tag_name": "v1.0.19", "name": "Version 1.0.19 - Hotfix"},
        {"tag_name": "v1.0.18", "name": "Version 1.0.18 - Current"},
    ]


def mock_download_success():
    """
    Simulates successful download without actually downloading
    Returns tuple: (success: bool, message: str)
    """
    logger.info("🎭 MOCK: Simulating successful download...")
    logger.info("🎭 MOCK: No actual files were downloaded")
    return True, "Mock update installed successfully (no files changed)"


def mock_download_failure():
    """
    Simulates download failure for error handling testing
    """
    logger.error("🎭 MOCK: Simulating download failure...")
    from ..exception.model.lspotato_exceptions import DownloadException
    raise DownloadException(
        "https://mock.github.com/download",
        "Mock download failure for testing error handling"
    )


# ============================================
# INTEGRATION NOTES
# ============================================

"""
TO ENABLE MOCK MODE:
====================

In utils.py, add this at the start of check_for_updates():

    # ========================================
    # FOR TESTING ONLY - REMOVE IN PRODUCTION
    # ========================================
    from .mock_update_data import get_mock_update_data
    return get_mock_update_data()
    # ========================================
    # END MOCK DATA
    # ========================================

TO DISABLE MOCK MODE:
=====================
Simply comment out or remove the lines above.

TESTING WORKFLOW:
=================
1. Enable mock mode in utils.py
2. Change ACTIVE_SCENARIO in this file
3. Restart Blender addon
4. Click "Check for Updates"
5. Verify popup behavior
6. Test all scenarios
7. Disable mock mode before release

PRODUCTION CHECKLIST:
=====================
[ ] Remove/comment mock data import in utils.py
[ ] Verify actual GitHub API calls work
[ ] Test with real network conditions
[ ] Verify version comparison logic with real releases
[ ] Test edge cases (no internet, API rate limit, etc.)
"""