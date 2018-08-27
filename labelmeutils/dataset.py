import glob
import json
import os

from .utils import load_json
from .utils import load_image


class LabelMeDataset(object):

    def __init__(self, root):
        self.root = root
        self.label_paths = self._get_vaild_label_paths()

    def __getitem__(self, index):
        # label
        label_path = self.label_paths[index]

        label_dict = load_json(label_path)
        shapes = label_dict['shapes']

        # image
        image_path = os.path.join(self.root, label_dict['imagePath'])
        image = load_image(image_path)

        return image, shapes

    def __len__(self):
        return len(self.images)

    def _get_vaild_label_paths(self):
        label_paths = []

        paths = glob.glob(os.path.join(self.root, '*.json'))

        for path in paths:
            try:
                label_dict = load_json(path)
            except json.decoder.JSONDecodeError:
                continue

            image_path = os.path.join(self.root, label_dict['imagePath'])
            if os.path.exists(image_path):
                label_paths.append(path)

        return label_paths
