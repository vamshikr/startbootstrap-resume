#! /usr/bin/env python3

set -o nounset
set -o errexit
set -o pipefail


function is_valid {
  local FILE_PATH="$1"

  if [[ -f "$FILE_PATH" && "$FILE_PATH" =~ .+[.]zip ]]; then
    return 0
  else
    return 1
  fi

}

function  main {
  #statements
  local FILE_PATH="$1"
  local VALID_FILES=(Courses.csv Honors.csv Skills.csv Profile.csv Certifications.csv Education.csv Learning.csv Positions.csv Languages.csv Projects.csv)

  if ! $(is_valid "$FILE_PATH"); then
    echo "Invalid $FILE_PATH file" && exit 1;
  fi

  local NEW_FILE_PATH="${FILE_PATH%.zip}-copy.zip"

  zip -U "$FILE_PATH" ${VALID_FILES[@]} --out "$NEW_FILE_PATH" && echo "Created a new archive $NEW_FILE_PATH"

}

#set -x;
main "$@"
