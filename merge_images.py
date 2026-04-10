"""이미지를 방향과 갭을 지정하여 합쳐주는 스크립트"""

import argparse
from pathlib import Path
from PIL import Image


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
        # 가로 합치기: 높이를 최대값에 맞춰 비율 리사이즈
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
        # 세로 합치기: 너비를 최대값에 맞춰 비율 리사이즈
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
    parser.add_argument("images", nargs="+", help="합칠 이미지 파일들")
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

    for p in args.images:
        if not Path(p).exists():
            parser.error(f"파일을 찾을 수 없습니다 - {p}")

    merge_images(args.images, args.output, args.direction, args.gap_x, args.gap_y)


if __name__ == "__main__":
    main()
