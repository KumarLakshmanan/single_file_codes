#!/usr/bin/env python3
"""
upload_images.py

Usage:
 - Run the script and enter a folder path when prompted (e.g. `pmschool` or `pmschool/I-A`).
 - The script will list class folders, student folders and show `data.json` contents.
 - You'll be prompted whether to upload images found in `data.json` to the server.

This mirrors the upload flow used by the Flutter app (calls `getstdidcarddetails` then `upload.php`).

Note: requires `requests` library: `pip install requests`
"""

import os
import sys
import json
import requests
from pathlib import Path

# Constants copied from the Flutter project's `lib/constant.dart`
API_URL = "https://secid2.nirals.in/jarvisv2.php"
UPLOAD_URL = "https://secid2.nirals.in/upload.php"
APIKEY = "Q1gL3qrN2hnigGvT"
APIID = "2510"
CMPNY = "nirals"

WORKSPACE_ROOT = Path(__file__).resolve().parent


def resolve_path(p: str, base_school: str = None) -> Path:
    """Resolve a path coming from data.json to a local path in this repo when possible.

    The app stores Android file paths like '/storage/emulated/0/SecID/...'.
    This function will try that path first; if not found, it will replace
    '/storage/emulated/0/SecID' with the repository root and try again.
    """
    p = str(p)
    cand = Path(p)
    if cand.exists():
        return cand
    # try mapping Android SecID path to workspace
    android_prefix = '/storage/emulated/0/SecID'
    if p.startswith(android_prefix):
        remainder = p[len(android_prefix) + 1:]
        # remainder starts with the school folder name from device (e.g. 'pmarts/...')
        parts = remainder.split(os.sep)
        if len(parts) >= 2:
            # drop the original school folder from device path and use base_school if provided
            rest_after_school = os.sep.join(parts[1:])
            if base_school:
                mapped = WORKSPACE_ROOT / base_school / rest_after_school
            else:
                mapped = WORKSPACE_ROOT / remainder
        else:
            mapped = WORKSPACE_ROOT / remainder
        if mapped.exists():
            return mapped
    # try relative
    rel = WORKSPACE_ROOT / p
    if rel.exists():
        return rel
    return cand  # best effort


def post_get_std_details(cls, selschool, stdid, passcode):
    payload = {
        'mode': 'getstdidcarddetails',
        'cls': cls,
        'selschool': selschool,
        'stdid': stdid,
        'passcode': passcode,
        'company_code': CMPNY,
        'apikey': APIKEY,
        'apiid': APIID,
    }
    try:
        r = requests.post(API_URL, data=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] getstdidcarddetails request failed: {e}")
        return None


def post_upload_file(file_path, cls, selschool, stdid, passcode):
    data = {
        'mode': 'uploadidimage',
        'cls': cls,
        'selschool': selschool,
        'passcode': passcode,
        'dir': f'data/nirals/{selschool}/idimages/',
        'stdid': stdid,
        'cmpny_code': CMPNY,
        'apikey': APIKEY,
        'apiid': APIID,
    }
    files = {}
    try:
        with open(file_path, 'rb') as fh:
            files['erpFileInput[]'] = (os.path.basename(file_path), fh)
            r = requests.post(UPLOAD_URL, data=data, files=files, timeout=60)
            r.raise_for_status()
            return r.text
    except Exception as e:
        print(f"[ERROR] upload failed for {file_path}: {e}")
        return None


def list_folder(base_path: Path):
    print(f"Listing contents of: {base_path}\n")
    if not base_path.exists():
        print("Path does not exist.")
        return []
    classes = []
    for cls in sorted([p for p in base_path.iterdir() if p.is_dir()]):
        print(f"Class: {cls.name}")
        classes.append(cls)
        for student in sorted([s for s in cls.iterdir() if s.is_dir()]):
            print(f"  Student: {student.name}")
            data_json = student / 'data.json'
            if data_json.exists():
                print(f"    data.json found: {data_json}")
                try:
                    with open(data_json, 'r', encoding='utf-8') as f:
                        entries = json.load(f)
                    for i, e in enumerate(entries):
                        print(f"      [{i}] file={e.get('file')} stdid={e.get('stdid')} isUploaded={e.get('isUploaded')}")
                except Exception as e:
                    print(f"      Could not read data.json: {e}")
            else:
                print("    data.json NOT found")
    return classes


def summarize_folder(base_path: Path):
    """Return and print a concise summary: number of student folders and total photos across all data.json files."""
    total_students = 0
    students_with_data = 0
    total_photos = 0

    if not base_path.exists():
        print("Path does not exist.")
        return {
            'total_students': 0,
            'students_with_data': 0,
            'total_photos': 0,
        }

    for cls in sorted([p for p in base_path.iterdir() if p.is_dir()]):
        for student in sorted([s for s in cls.iterdir() if s.is_dir()]):
            total_students += 1
            data_json = student / 'data.json'
            if data_json.exists():
                students_with_data += 1
                try:
                    with open(data_json, 'r', encoding='utf-8') as f:
                        entries = json.load(f)
                    total_photos += len(entries)
                except Exception:
                    # ignore malformed files for the summary
                    pass

    print(f"Students found: {total_students}")
    print(f"Students with data.json: {students_with_data}")
    print(f"Total photos (data.json entries): {total_photos}")

    return {
        'total_students': total_students,
        'students_with_data': students_with_data,
        'total_photos': total_photos,
    }


def process_and_upload(base_path: Path):
    classes = [p for p in base_path.iterdir() if p.is_dir()]
    for cls in sorted(classes):
        for student in sorted([s for s in cls.iterdir() if s.is_dir()]):
            data_json = student / 'data.json'
            if not data_json.exists():
                continue
            try:
                with open(data_json, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except Exception as e:
                print(f"[ERROR] Reading {data_json}: {e}")
                continue

            updated = False
            for i, e in enumerate(entries):
                file_in_json = e.get('file')
                stdid = e.get('stdid')
                classname = e.get('classname') or cls.name
                schoolid = e.get('schoolid')
                password = e.get('password')
                is_uploaded = e.get('isUploaded', False)

                # Previously we skipped entries already marked uploaded.
                # User requested we attempt upload even if `isUploaded` is true.
                if is_uploaded:
                    print(f"Note: entry already marked uploaded, attempting re-upload: {file_in_json}")

                print(f"\nProcessing {student.name} -> {file_in_json}")

                # Resolve path locally using the base school name supplied by the user
                base_school = base_path.name
                resolve_p = resolve_path(file_in_json, base_school=base_school)
                if not resolve_p.exists():
                    print(f"  Local file not found: {resolve_p}")
                    continue

                # Check server-side status first (mirror Flutter logic)
                details = post_get_std_details(classname, schoolid, stdid, password)
                if not details:
                    print("  Could not fetch student details; skipping upload.")
                    continue
                try:
                    status = details['data'][stdid]['STATUS']
                except Exception:
                    print("  Unexpected response format from getstdidcarddetails; skipping.")
                    continue

                if str(status) not in ("0", "1"):
                    print(f"  Student status indicates already approved (STATUS={status}); skipping upload.")
                    continue

                # Upload
                print(f"  Uploading {resolve_p} ...")
                resp = post_upload_file(str(resolve_p), classname, schoolid, stdid, password)
                if resp is None:
                    print("  Upload request failed.")
                else:
                    print(f"  Upload response: {resp[:200]}")
                    # Mark as uploaded in data.json
                    entries[i]['isUploaded'] = True
                    updated = True

            if updated:
                try:
                    with open(data_json, 'w', encoding='utf-8') as f:
                        json.dump(entries, f, indent=2)
                    print(f"  Updated {data_json} -> marked uploaded entries.")
                except Exception as e:
                    print(f"  Failed to update {data_json}: {e}")


def main():
    print("Enter folder path (relative to project root or absolute). Examples: 'pmschool' or 'pmschool/I-A'\n")
    inp = input("Folder: ").strip()
    if not inp:
        print("No folder provided, exiting.")
        return

    # Resolve the input path: absolute or relative to workspace root
    p = Path(inp)
    if not p.is_absolute():
        p = WORKSPACE_ROOT / inp

    if not p.exists():
        print(f"Path does not exist: {p}")
        return

    # Show concise summary counts
    summarize_folder(p)

    # Optionally show detailed listing
    show_details = input("\nShow detailed listing of students and data.json entries (y/n)? ").strip().lower()
    if show_details in ('y', 'yes'):
        list_folder(p)

    # Ask to upload
    do_upload = input("\nUpload images found in data.json (y/n)? ").strip().lower()
    if do_upload in ('y', 'yes'):
        process_and_upload(p)
    else:
        print("Skipping upload. Done.")


if __name__ == '__main__':
    main()
