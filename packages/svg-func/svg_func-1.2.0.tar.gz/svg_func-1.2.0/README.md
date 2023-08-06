# svg_func

<!-- Add buttons here -->

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/xieMNll/svg_func?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/xieMNll/svg_func)
![GitHub issues](https://img.shields.io/github/issues-raw/xieMNll/svg_func)
![GitHub pull requests](https://img.shields.io/github/issues-pr/xieMNll/svg_func)
![GitHub](https://img.shields.io/github/license/xieMNll/svg_func)

<!-- Describe your project in brief -->

The project is used for handle some computation in svg, like interpolation and envelope warp.


# Installation
[(Back to top)](#table-of-contents)

*
```git init```

```git clone https://github.com/xieMNll/svg_func.git```

or 

```pip install svg_func```

# Usage
[(Back to top)](#table-of-contents)

for example, envelope warp:
```shell
import interpolation
from interpolation import envelope_warp

svg_path = 'test.svg'
svg, xml = envelope_warp.main(svg_path,filetype='path',file_path='result.svg')
```
* in envelope_warp.main():

    :param svgpath: 输入svg，可以3种格式，根据 filetype
    
    :param sample_n: 默认10  svg中每个cmd的取点数，对点做坐标计算。点越多越平滑，
    
    :param filetype: 默认path   'url'是文件的url地址，'path'本地svg文件， 'string'是直接字符串输入，
    
    :param c_svg: 默认None  如果用于四边形封套。需输入文件矩形四个角点的target位置，[4,2],按左下角为原点的坐标系角点顺序为（左上角，左下角，右下角，右上角）; 
    如果用于random轮廓，轮廓的输入数据，格式与输入svg一致，可以是‘url','path','string'
    
    :param arch_per: 默认0.3 arch效果拱的程度 1~100%
    
    :param pos: 默认up 朝哪个方向拱，分别有'up' 'left' 'right' 'down'
    
    :param fix: 暂时不使用
    
    :param mode:默认arch  一共有5种 'arch' 'single_arch' 'polygon' 'circle','random'
    
    :param file_path:默认None 结果svg存储路径
    
    :return: 返回svg的字符串。两种方式做出。第一种是完全自己写， 第二种是只改变d中的数据。 一般只用第二个结果
