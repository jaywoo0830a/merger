"""이미지를 방향과 갭을 지정하여 합쳐주는 스크립트"""

import argparse
import re
from pathlib import Path
from PIL import Image

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def natural_sort_key(path: Path):
    """파일명을 자연 정렬 (1, 2, 10 순)"""
    return [
        int(s) if s.isdigit() else s.lower()
        for s in re.split(r"(\d+)", path.name)
    ]


def collect_images(path: str) -> list[str]:
    """파일 또는 디렉토리에서 이미지 경로 목록 반환"""
    p = Path(path)
    if p.is_dir():
        files = sorted(
            [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
            key=natural_sort_key,
        )
        return [str(f) for f in files]
    return [str(p)]


def merge_images(
    image_paths: list[str],
    output_path: str,
    direction: str = "tb",
    gap_x: int = 0,
    gap_y: int = 0,
) -> None:
    images = [Image.open(p) for p in image_paths]
    horizontal = direction in ("lr", "rl")

    if horizontal:
        max_height = max(img.height for img in images)
        resized = []
        for img in images:
            if img.height != max_height:
                ratio = max_height / img.height
                img = img.resize((int(img.width * ratio), max_height), Image.LANCZOS)
            resized.append(img)

        if direction == "rl":
            resized.reverse()

        total_width = sum(img.width for img in resized) + gap_x * (len(resized) - 1)
        canvas_w, canvas_h = total_width, max_height
        result = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

        x_offset = 0
        for img in resized:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            result.paste(img, (x_offset, 0))
            x_offset += img.width + gap_x
    else:
        max_width = max(img.width for img in images)
        resized = []
        for img in images:
            if img.width != max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
            resized.append(img)

        if direction == "bt":
            resized.reverse()

        total_height = sum(img.height for img in resized) + gap_y * (len(resized) - 1)
        canvas_w, canvas_h = max_width, total_height
        result = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

        y_offset = 0
        for img in resized:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            result.paste(img, (0, y_offset))
            y_offset += img.height + gap_y

    if output_path.lower().endswith((".jpg", ".jpeg")):
        result = result.convert("RGB")

    result.save(output_path)
    print(f"저장 완료: {output_path} ({canvas_w}x{canvas_h})")


def main():
    parser = argparse.ArgumentParser(description="이미지를 합쳐주는 스크립트")
    parser.add_argument(
        "inputs", nargs="+",
        help="합칠 이미지 파일 또는 디렉토리 (디렉토리 지정 시 내부 이미지를 자연 정렬하여 사용)",
    )
    parser.add_argument("-o", "--output", required=True, help="출력 파일 경로")
    parser.add_argument(
        "-d", "--direction",
        choices=["lr", "rl", "tb", "bt"],
        default="tb",
        help="합치는 방향: lr(좌→우), rl(우→좌), tb(위→아래), bt(아래→위) (기본: tb)",
    )
    parser.add_argument("--gap-x", type=int, default=0, help="X축 갭 (px, 기본: 0)")
    parser.add_argument("--gap-y", type=int, default=0, help="Y축 갭 (px, 기본: 0)")

    args = parser.parse_args()

    image_paths = []
    for inp in args.inputs:
        if not Path(inp).exists():
            parser.error(f"파일을 찾을 수 없습니다 - {inp}")
        image_paths.extend(collect_images(inp))

    if len(image_paths) < 2:
        parser.error("합칠 이미지가 2개 이상 필요합니다.")

    print(f"합칠 이미지 {len(image_paths)}개:")
    for p in image_paths:
        print(f"  {p}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    merge_images(image_paths, args.output, args.direction, args.gap_x, args.gap_y)


if __name__ == "__main__":
    main()
