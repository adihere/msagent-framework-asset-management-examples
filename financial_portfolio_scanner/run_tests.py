#!/usr/bin/env python3
"""
Test Runner Script for Financial Portfolio Scanner

This script discovers and runs all tests using pytest, provides a summary of test results,
and returns appropriate exit codes for CI/CD integration. It includes command-line options
for test configuration such as verbose output and coverage reporting.
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path


def parse_arguments():
    """Parse command-line arguments for the test runner."""
    parser = argparse.ArgumentParser(
        description="Run tests for the Financial Portfolio Scanner project"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    
    parser.add_argument(
        "--cov-report",
        choices=["html", "term", "xml"],
        default="term",
        help="Coverage report format (default: term)"
    )
    
    parser.add_argument(
        "--cov-fail-under",
        type=int,
        default=80,
        help="Coverage percentage threshold for failure (default: 80)"
    )
    
    parser.add_argument(
        "-x", "--stop-on-fail",
        action="store_true",
        help="Stop test execution on first failure"
    )
    
    parser.add_argument(
        "-k", "--keyword",
        type=str,
        help="Only run tests matching the given keyword expression"
    )
    
    parser.add_argument(
        "--test-path",
        type=str,
        default="tests",
        help="Path to the test directory (default: tests)"
    )
    
    return parser.parse_args()


def build_pytest_command(args):
    """Build the pytest command based on the provided arguments."""
    cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.stop_on_fail:
        cmd.append("-x")
    
    if args.keyword:
        cmd.extend(["-k", args.keyword])
    
    if args.coverage:
        cmd.extend(["--cov=.", f"--cov-report={args.cov_report}", f"--cov-fail-under={args.cov_fail_under}"])
    
    # Add the test path
    cmd.append(args.test_path)
    
    return cmd


def run_tests(cmd):
    """Execute the pytest command and return the results."""
    try:
        # Change to the project directory
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # Run the tests
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def print_summary(stdout, stderr, exit_code):
    """Print a summary of the test results."""
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    
    if stdout:
        print("\nSTDOUT:")
        print(stdout)
    
    if stderr:
        print("\nSTDERR:")
        print(stderr)
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("RESULT: ALL TESTS PASSED [OK]")
    else:
        print("RESULT: TESTS FAILED [FAIL]")
    print("="*60)
    
    return exit_code


def main():
    """Main function to run the test script."""
    args = parse_arguments()
    cmd = build_pytest_command(args)
    
    print(f"Running tests with command: {' '.join(cmd)}")
    print("-" * 60)
    
    exit_code, stdout, stderr = run_tests(cmd)
    
    # Print summary and return the exit code
    return print_summary(stdout, stderr, exit_code)


if __name__ == "__main__":
    sys.exit(main())