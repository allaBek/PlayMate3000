## Description
This class contains functions made to perform the operations needed throughout 
the the process of the vision system of Playmate3000.
The class includes three main functions : --reArrange-- , --getCorners-- and --imageSlices--

#### reArrange(matrix,r,c)
the funtion --reArrange-- does the job of taking a --matrix-- containing pair elements (x and y, as an image array of pixels)
and its rows --r-- and columns --c-- as an input and gives a sorted matrix in ascending order as an output.

#### example
let try re-arranging the next 8x8 matrix
```

map=[
    [10, 15],[7, 5],[6, 23],[9, 43],[44, 9],[21, 3],[34, 100],[23,55],
    [89, 67],[1, 67],[134, 89],[89, 56],[43, 76],[32, 12],[133, 12],[91, 66],
    [9, 8], [51, 15], [15, 71], [17, 98], [23, 92], [167, 157], [135, 126], [126, 67],
    [10, 15], [8, 16], [6, 23], [9, 43], [44, 9], [21, 3], [34, 100], [23, 55],
    [89, 67], [1, 67], [134, 89], [89, 56], [43, 76], [32, 12], [133, 12], [91, 66],
    [9, 8], [51, 15], [66, 23], [17, 98], [23, 92], [167, 157], [135, 126], [126, 67],
    [10, 15], [8, 16], [6, 23], [9, 43], [44, 9], [21, 3], [34, 100], [23, 55],
    [89, 67], [1, 67], [134, 89], [89, 56], [43, 76], [32, 12], [133, 12], [91, 66],
]
```

so simply we give the inputs for the function as:
--reArrange(map,8,8)--

the output would be:
```
[
[[7, 5], [9, 8], [21, 3], [32, 12], [44, 9], [51, 15], [133, 12], [133, 12]],
[[8, 16], [9, 8], [21, 3], [32, 12], [44, 9], [51, 15], [133, 12], [134, 89]],
[[6, 23], [10, 15], [21, 3], [32, 12], [44, 9], [66, 23], [89, 56], [134, 89]],
[[6, 23], [10, 15], [10, 15], [23, 55], [43, 76], [89, 56], [91, 66], [134, 89]],
[[6, 23], [8, 16], [23, 55], [23, 55], [43, 76], [89, 56], [91, 66], [135, 126]],
[[1, 67], [9, 43], [15, 71], [23, 92], [43, 76], [89, 67], [91, 66], [135, 126]], 
[[1, 67], [9, 43], [17, 98], [23, 92], [34, 100], [89, 67], [126, 67], [167, 157]],
[[1, 67], [9, 43], [17, 98], [34, 100], [34, 100], [89, 67], [126, 67], [167, 157]]
]
```


as we see, it is arranged based on both the x and y axis, as an array of pixels in image.



#### getCorners(mapped)




