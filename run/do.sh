#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
source "$SCRIPT_DIR/.venv/bin/activate"

ASSETS_DIR="$SCRIPT_DIR/assets"
RESULT_DIR="$ASSETS_DIR/result"

mkdir -p "$RESULT_DIR"

# assets/ 최상위의 이미지 파일 수집 (하위 디렉토리 제외)
images=()
for f in "$ASSETS_DIR"/*.{png,jpg,jpeg,gif,bmp,webp}; do
    [ -f "$f" ] && images+=("$f")
done

if [ ${#images[@]} -eq 0 ]; then
    echo "오류: assets/ 에 이미지 파일이 없습니다."
    exit 1
fi

# 파일명 기준 정렬
IFS=$'\n' images=($(sort -V <<<"${images[*]}")); unset IFS

echo "합칠 이미지 ${#images[@]}개:"
printf '  %s\n' "${images[@]}"

# do.sh 이후의 인자를 그대로 merge_images.py에 전달
python3 "$SCRIPT_DIR/merge_images.py" "${images[@]}" -o "$RESULT_DIR/merged.png" "$@"
