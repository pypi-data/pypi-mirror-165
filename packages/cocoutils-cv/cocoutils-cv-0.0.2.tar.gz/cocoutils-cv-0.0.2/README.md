

# cocoutils

This tool is mainly for visual analysis of coco datasets, which is divided into three modules: Analyzer, Checker, Transfer, currently only supporting the object detection format;

### Install

```
pip install cocoutils-cv
```



### Usage

```
from cocoutils import Analyzer, Checker, Transfer
```



#### 1、**Analyzer**

For visual analysis of COCO datasets, there are 11 analysis charts;

**Demo:**

```
Analyzer("coco.json")
```

**Paras:**

    """
    Analyze coco datasets through charts
    :param coco_path (str) : the path of Coco format JSON file
    :param save_path (dir) : the dir to save the chart, if None, it will display directly on the desktop
    :param map_size (int)  : Determine the number of heatmap grids
    """

（1）General information：Count the number of images, targets and categories

![General information](analysis_result\General information.jpg)

（2）Image size number：Number of images per size

![Image size number](analysis_result\Image size number.jpg)

（3）Number of targets per picture：Target number of images per image

![Number of targets per picture](analysis_result\Number of targets per picture.jpg)

（4）Number of pictures in each category：The number of each category

![Number of pictures in each category](analysis_result\Number of pictures in each category.jpg)

（5）Quantity proportion of each category：Proportion of each category

![Quantity proportion of each category](analysis_result\Quantity proportion of each category.jpg)

（6）Number of each category：The number of targets contained in each category

![Number of each category](analysis_result\Number of each category.jpg)

（7）Absolute target area：Target size category distribution:（Small <32x32, Big > 96x96, the rest is medium）

![Absolute target area](analysis_result\Absolute target area.jpg)

（8）Object area distribution：Object absolute area distribution (L x W)

![Object area distribution](analysis_result\Object area distribution.jpg)

（9）Object relative area distribution：Target relative area distribution, (target area/image area)

![Object relative area distribution](analysis_result\Object relative area distribution.jpg)

（10）Aspect ratio distribution：Target aspect ratio distribution

![Aspect ratio distribution](analysis_result\Aspect ratio distribution.jpg)

（11）Object position distribution：The number of target centers distributed on the image

![Object position distribution](analysis_result\Object position distribution.jpg)



#### 2、**Checker**

Check the data set annotation format, visual analysis and repair, (repair only supports filtering images without annotations and error annotations will be forced to limit the scope of the image)

**Demo:**

```
coco = "coco.json"
repair_coco = "repair_coco.json"
img_dir = "result"
img_id = 2

check = Checker(coco)

check.drawImg(img_id)

check.check()

check.repair(repair_coco)
```

**Paras：**

```
def __init__(self, coco_path):
    """
    Check dataset outliers and visualization
    :param coco_path (str) : the path of Coco format JSON file
    """
```

```
def drawImg(self, img_dir, img_id, save_dir=None):
    """
    Draw annotations through image index
    :param img_dir (str) : picture save folder
    :param img_id (int) : image id
    :param save_dir (int) : save the picture folder after drawing, if None, it will display directly on the desktop
    """
```

```
def check(self, img_dir=None, log="check.txt"):
    """
    Check annotations and pictures
    :param img_dir (str) : picture save folder, if None, do not check whether the picture exists
    :param log (path) : address to save inspection results
    """
```

```：：
def repair(self, save_path, img_dir=None):
    """
    Repair annotations
    :param save_path (str) : save the repaired coco address
    :param img_dir (str) : picture save folder, if None, do not check whether the picture exists
    """
```





#### 3、**Transfer**

Data set format conversion, support Custom2COCO, YOLO2COCO, Labelme2Coco, VOC2Coco, merge coco dataset

**Demo:**

```
labelme_dir = r"test"
dst_coco = "coco.json"
transfer = Transfer
transfer.lableme2coco(dst_coco, labelme_dir)
```

**Paras:**

```
def custom(self, dst_coco, img_abs_paths, cats, bboxes):
    """
    Custom dataset conversion to coco format
    :param dst_coco (str) : the path of Coco format JSON file to save
    :param img_abs_pathsh (list) : picture absolute address list, ["path/to/img1.jpg", "path/to/img2.jpg",...]
    :param img_abs_pathsh (list) : category name list, [["cat1","cat1","cat2"], ["cat2"],...]
    :param bboxes (list)  : xywh list, [[xywh1,xywh2,xyw3], [xywh4],...]
    The three must match one by one
    """
```

```
def lableme2coco(self, dst_coco, labelme_dir):
    """
    Labelme format to coco format
    :param dst_coco (str) : the path of Coco format JSON file to save
    :param labelme_dir (str) : JSON file folder
    """
```

```
def voc2coco(self, dst_coco, xml_dir):
    """
    voc format to coco format
    :param dst_coco (str) : the path of Coco format JSON file to save
    :param xml_dir (str) : XML file folder
    """
```

```
def yolo2coco(self, dst_coco, txt_dir,  img_dir, cat_names=None):
    """
    yolo txt format to coco format
    :param dst_coco (str) : the path of Coco format JSON file to save
    :param txt_dir (str) : txt file folder
    :param img_dir (str) : picture folder
    :param cat_names (list) : specify category name, if None, use index as name
    """
```

```
def mergeCoco(self, dst_coco, main_coco, second_coco):
    """
    Merge two coco datasets
    :param dst_coco (str) : the path of Coco format JSON file to save
    :param main_coco (str) : the path of Coco, as head
    :param second_coco (str) : the path of Coco, as tail
    """
```

