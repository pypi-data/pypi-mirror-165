import sys

from pdf2image import convert_from_path


BITMAP_WIDTH = 420
BUCKETS = 256


def measure_image_darkness(image):
    hist = image.histogram()
    r, g, b = hist[:BUCKETS], hist[BUCKETS:BUCKETS * 2], hist[BUCKETS * 2:]
    total = 0
    weighted_sum = 0.0
    for counts in [r, g, b]:
        for _, count in enumerate(counts):
            total += count
            weighted_sum += _ / (BUCKETS - 1) * count
    return 1.0 - weighted_sum / total


def measure_pdf_darkness(pdf_path):
    images = convert_from_path(pdf_path)
    return [
        measure_image_darkness(image.resize((BITMAP_WIDTH, BITMAP_WIDTH * image.height // image.width))) for page, image in enumerate(images)
    ]


def main():
    for pdf_path in sys.argv[1:]:
        try:
            for page, darkness in enumerate(measure_pdf_darkness(pdf_path)):
                print(pdf_path, page + 1, f"{darkness:.8f}", sep="\t")
        except Exception as e:
            print(pdf_path, "failed", e, sep="\t") 


if __name__ == "__main__":
    main()
