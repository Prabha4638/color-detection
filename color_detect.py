# pip install pandas opencv-python

import cv2
import pandas as pd

# --------------------------------------------------------

# Your Previous File Names
img_path = 'sample.jpg'
csv_path = 'colors.csv'

# Reading CSV File
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Reading Image
img = cv2.imread(img_path)

# Resize Image
img = cv2.resize(img, (800, 600))

# Create Copy of Original Image
img_copy = img.copy()

# Global Variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to Get Color Name
def get_color_name(R, G, B):

    minimum = 1000

    for i in range(len(df)):

        d = abs(R - int(df.loc[i, "R"])) + \
            abs(G - int(df.loc[i, "G"])) + \
            abs(B - int(df.loc[i, "B"]))

        if d <= minimum:
            minimum = d
            cname = df.loc[i, "color_name"]

    return cname

# Mouse Double Click Function
def draw_function(event, x, y, flags, param):

    global b, g, r, xpos, ypos, clicked

    if event == cv2.EVENT_LBUTTONDBLCLK:

        clicked = True

        xpos = x
        ypos = y

        b, g, r = img_copy[y, x]

        b = int(b)
        g = int(g)
        r = int(r)

# Create Window
cv2.namedWindow('Color Detection Project')

# Mouse Callback
cv2.setMouseCallback('Color Detection Project', draw_function)

# Main Loop
while True:

    # Create Fresh Copy Every Time
    display_img = img_copy.copy()

    if clicked:

        # Draw Circle Marker at Click Position
        cv2.circle(display_img, (xpos, ypos), 8, (0, 0, 255), -1)

        # Draw Small Cross Lines
        cv2.line(display_img, (xpos - 15, ypos), (xpos + 15, ypos), (255, 255, 255), 2)
        cv2.line(display_img, (xpos, ypos - 15), (xpos, ypos + 15), (255, 255, 255), 2)

        # Draw Rectangle for Color Info
        cv2.rectangle(display_img, (20, 20), (780, 70), (b, g, r), -1)

        # Create Text
        text = get_color_name(r, g, b) + \
               '  R=' + str(r) + \
               ' G=' + str(g) + \
               ' B=' + str(b)

        # Text Color
        text_color = (255, 255, 255)

        if r + g + b >= 600:
            text_color = (0, 0, 0)

        # Display Text
        cv2.putText(display_img,
                    text,
                    (50, 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    text_color,
                    2,
                    cv2.LINE_AA)

    # Show Image
    cv2.imshow("Color Detection Project", display_img)

    # Press ESC to Exit
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()