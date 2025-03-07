import io
import cv2
import sys
import numpy as np
from PIL import Image


def main():
    try:
        raw_file = sys.argv[1]
        output_file_name = sys.argv[2]
        raw_image = Image.open(raw_file)
        name_list = output_file_name.split(".")
    except IndexError:
        print("Error opening input: Enter the input file name and output file name")
        sys.exit(1)
    except FileNotFoundError:
        print("Error opening input: File not found")
        sys.exit(1)

    buffer = io.BytesIO()
    try:
        raw_image.save(buffer, format=name_list[1])
    except Exception as e:
        print("Error opening input: ", e)
        sys.exit(1)

    converted_file = buffer.getvalue()
    image = image_slice(converted_file, output_file_name)
    image.slice()


class image_slice:
    def __init__(self, image, output):
        self.image = image
        self.slice_list = np.empty([4,4], dtype=object)
        self.over_slice = np.empty([2], dtype=object)
        self.output = output

    def slice(self):
        img = cv2.imdecode(np.frombuffer(self.image, np.uint8), cv2.IMREAD_COLOR)

        self.over_slice[0] = img[0:1184, 800:822]
        self.over_slice[1] = img[1184:1200, 0:822]

        height, width = 1184, 800
        x, y = 0, 0
        for i in range(4):
            for j in range(4):
                self.slice_list[i][j] = img[y:y+height//4, x:x+width//4]
                x += width//4
            x = 0
            y += height//4
        
        def coupling():
            list_T = self.slice_list.T
            row = []
            for i in range(4):
                row.append(cv2.hconcat([list_T[i][0], list_T[i][1], list_T[i][2], list_T[i][3]]))
            col = cv2.vconcat(row)
            h_image = cv2.hconcat([col, self.over_slice[0]])
            true_image = cv2.vconcat([h_image, self.over_slice[1]])

            cv2.imwrite(self.output, true_image)
        
        coupling()


if __name__ == "__main__":
    main()