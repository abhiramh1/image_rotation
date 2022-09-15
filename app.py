""" As per the current MVP design, the application allows the users to rotate the image (pbm) in specific angle
that is predefined (90, 180, 270) in a clockwise or anti-clockwise manner. """

from os import listdir

SOURCE_FILES_PATH = "source_images/"
ACCEPTED_FILE_FORMAT = ".pbm"
PORTABLE_BITMAP_FORMAT = "P1"

ORIENTATION_ANGLE_90 = 1
ORIENTATION_ANGLE_180 = 2
ORIENTATION_ANGLE_270 = 3

ORIENTATION_ANGLE_LIST_MASTER = {
    ORIENTATION_ANGLE_90: 90,
    ORIENTATION_ANGLE_180: 180,
    ORIENTATION_ANGLE_270: 270
}

ORIENTATION_TYPE = {
    1: "Clockwise",
    2: "Anti - Clockwise"
}

ANTI_CLOCKWISE_MAPPING_TO_CLOCKWISE = {
    1: ORIENTATION_ANGLE_270,
    2: ORIENTATION_ANGLE_180,
    3: ORIENTATION_ANGLE_90
}


def generate_input_selection(input_list, message, error_message):
    try:
        for key, value in input_list.items():
            print(str(key) + ": " + str(value))
        identifier_key = input(message)
        if not identifier_key.isnumeric() and input_list.get(identifier_key) is None:
            raise ValueError(error_message)
        return identifier_key
    except ValueError as error:
        raise error


def get_orientation_angle_key(or_type):
    angle_key = generate_input_selection(ORIENTATION_ANGLE_LIST_MASTER, "Please input the angle of rotation: ",
                                         "Please enter a valid angle of rotation!!")
    if or_type == 2:
        angle_key = ANTI_CLOCKWISE_MAPPING_TO_CLOCKWISE[int(angle_key)]
    return angle_key


def get_orientation_type_key():
    return generate_input_selection(ORIENTATION_TYPE, "Please input the type of rotation: ",
                                    "Please enter a valid type of rotation!!")


def get_file_details_formatted_for_display():
    file_details = [f for f in listdir(SOURCE_FILES_PATH) if ACCEPTED_FILE_FORMAT in f]
    return {file_index + 1: file_name for file_index, file_name in enumerate(file_details)}


""" Function to display all the files (.pbm) format available in the source image folder, 
so the user can select the desired file to be rotated """


def get_file_input():
    try:
        file_details = get_file_details_formatted_for_display()
        for key, value in file_details.items():
            print(str(key) + ": " + value)
        file_key = input("Please input the number corresponding to the file name: ")
        if not file_key.isnumeric() and file_details.get(file_key) is None:
            raise ValueError("Please enter a valid image number from the above list!!")
        return file_details.get(int(file_key))
    except ValueError as error:
        raise error


""" Create the rotated file and save to the folder """


def create_file(file_name, file_content):
    file_path = "rotated_images/updated_" + file_name
    with open(file_path, "w") as f:
        f.write(file_content)
    return file_path


""" Create the binary content of .pbm file with P1 format """


def format_updated_image(pbm_format, width, height, array_details):
    image_raw = ""
    image_raw += pbm_format + "\n"
    image_raw += "# converted image" + "\n"
    image_raw += str(width) + " " + str(height) + "\n"
    for inner_array in array_details:
        inner_str_raw_image = " ".join(str(x) for x in inner_array)
        image_raw += inner_str_raw_image + "\n"
    return image_raw


""" Common function that is in recursion. Same function can be user for both clockwise and anticlockwise rotation based
 on the value of total rec  """


def rotate_array_90_degree_clock(source_array, total_rec):
    updated_list = list(zip(*source_array[::-1]))
    if total_rec != 0:
        return rotate_array_90_degree_clock(updated_list, total_rec - 1)
    else:
        return updated_list


""" Index function where the main business logics are written  """


def index(file_name, orientation_angle):
    try:
        file_path = SOURCE_FILES_PATH + file_name
        with open(file_path, "r") as f:
            image_internal_array = []
            lines = f.readlines()
            if PORTABLE_BITMAP_FORMAT in lines[1]:
                raise ValueError("Only P1 format accepted!")
            line_details = lines[3:] if "#" in lines[1] else lines[2:]
            for line in line_details:
                t = list(map(int, line.strip().split()))
                image_internal_array.append(t)
        rotated_image_inner_list = rotate_array_90_degree_clock(image_internal_array, orientation_angle - 1)
        height = len(rotated_image_inner_list)
        width = len(rotated_image_inner_list[0])
        format_updated_image_content = format_updated_image(PORTABLE_BITMAP_FORMAT, width, height, rotated_image_inner_list)
        return create_file(file_name, format_updated_image_content)
    except ValueError as ex:
        raise ex


if __name__ == "__main__":
    try:
        # select the image to rotate
        image_to_rotate = get_file_input()

        # select orientation angle
        orientation_type_key = get_orientation_type_key()

        # select orientation angle
        orientation_angle_key = get_orientation_angle_key(orientation_type_key)

        # master method which handles the image rotation
        rotated_file_path = index(image_to_rotate, int(orientation_angle_key))

        print("Image rotated successfully. You can see the file here: " + rotated_file_path)
    except ValueError as e:
        print(str(e))
