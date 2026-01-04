"""
Test cases for version compatibility logic
"""

def is_compatible_version(current_version, latest_version):
    """
    Check if latest version is compatible with current version branch.
    Only updates within the same sub-version branch or next minor version.
    """
    current_major, current_minor, current_patch = current_version
    latest_major, latest_minor, latest_patch = latest_version
    
    # Same major version
    if current_major == latest_major:
        # Same minor version - allow any higher patch
        if current_minor == latest_minor:
            return latest_patch > current_patch
        
        # Next minor version or higher - allow
        if latest_minor == current_minor + 1:
            return True
        
        # Skip other minor versions (too far ahead)
        return False
    
    # Different major version - not compatible
    return False

def main():
    # Test cases
    test_cases = [
        # Format: (current, latest, expected_result, description)
        
        # Same sub-version branch - patch updates
        ((1, 0, 18), (1, 0, 19), True, "1.0.18 -> 1.0.19 ✓ (same branch, higher patch)"),
        ((1, 0, 18), (1, 0, 20), True, "1.0.18 -> 1.0.20 ✓ (same branch, higher patch)"),
        ((1, 0, 18), (1, 0, 18), False, "1.0.18 -> 1.0.18 ✗ (same version)"),
        ((1, 0, 18), (1, 0, 17), False, "1.0.18 -> 1.0.17 ✗ (downgrade)"),
        
        # Next minor version
        ((1, 0, 18), (1, 1, 0), True, "1.0.18 -> 1.1.0 ✓ (next minor version)"),
        ((1, 0, 18), (1, 1, 5), True, "1.0.18 -> 1.1.5 ✓ (next minor version)"),
        ((1, 1, 5), (1, 2, 0), True, "1.1.5 -> 1.2.0 ✓ (next minor version)"),
        
        # Skip minor versions (too far)
        ((1, 0, 18), (1, 2, 0), False, "1.0.18 -> 1.2.0 ✗ (skip 1.1.x branch)"),
        ((1, 0, 18), (1, 3, 0), False, "1.0.18 -> 1.3.0 ✗ (skip multiple branches)"),
        ((1, 1, 5), (1, 3, 0), False, "1.1.5 -> 1.3.0 ✗ (skip 1.2.x branch)"),
        
        # Different major version
        ((1, 0, 18), (2, 0, 0), False, "1.0.18 -> 2.0.0 ✗ (different major version)"),
        ((1, 5, 10), (2, 0, 0), False, "1.5.10 -> 2.0.0 ✗ (different major version)"),
        ((2, 0, 5), (1, 9, 0), False, "2.0.5 -> 1.9.0 ✗ (downgrade major)"),
        
        # Edge cases
        ((1, 0, 0), (1, 0, 1), True, "1.0.0 -> 1.0.1 ✓ (first patch)"),
        ((1, 0, 0), (1, 1, 0), True, "1.0.0 -> 1.1.0 ✓ (first minor bump)"),
        ((0, 1, 0), (0, 2, 0), True, "0.1.0 -> 0.2.0 ✓ (beta versions)"),
        ((0, 1, 5), (0, 1, 6), True, "0.1.5 -> 0.1.6 ✓ (beta patch)"),
    ]
    
    
    print("=" * 80)
    print("VERSION COMPATIBILITY TEST RESULTS")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for current, latest, expected, description in test_cases:
        result = is_compatible_version(current, latest)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {description}")
        if result != expected:
            print(f"       Expected: {expected}, Got: {result}")
    
    print()
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 80)
    
    
    # Real-world scenarios
    print("\n" + "=" * 80)
    print("REAL-WORLD UPDATE SCENARIOS")
    print("=" * 80)
    print()
    
    scenarios = [
        ("User on 1.0.18", (1, 0, 18), [
            ((1, 0, 19), "1.0.19 - Bug fix"),
            ((1, 0, 20), "1.0.20 - Bug fix"),
            ((1, 1, 0), "1.1.0 - New features"),
            ((1, 2, 0), "1.2.0 - Major features"),
            ((2, 0, 0), "2.0.0 - Breaking changes"),
        ]),
        ("User on 1.1.5", (1, 1, 5), [
            ((1, 1, 6), "1.1.6 - Bug fix"),
            ((1, 1, 10), "1.1.10 - Bug fix"),
            ((1, 2, 0), "1.2.0 - New features"),
            ((1, 3, 0), "1.3.0 - Major features"),
            ((2, 0, 0), "2.0.0 - Breaking changes"),
        ]),
    ]
    
    for scenario_name, current, updates in scenarios:
        print(f"\n{scenario_name}:")
        print("-" * 60)
        for latest, update_desc in updates:
            compatible = is_compatible_version(current, latest)
            status = "✓ CAN UPDATE" if compatible else "✗ BLOCKED"
            print(f"  {status}: {update_desc}")

if __name__ == "__main__":
    main()

