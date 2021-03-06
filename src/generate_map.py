import numpy as np
map = np.zeros((500,500))

def line(p0,p1):
    line_pixels = []
    if p1[0]<p0[0]:
        p = p0
        p0 = p1
        p1 = p
    deltax = p1[0]-p0[0]
    deltay = p1[1]-p0[1]
    if np.abs(deltax)>np.abs(deltay):    
        if deltax==0:
            return line_pixels
        deltaerr = np.abs(deltay/deltax)
        error = 0.0
        y = p0[1]
        for x in range(p0[0],p1[0]+1):
            line_pixels.append((x,y))
            error += deltaerr
            if error>=0.5:
                y += np.sign(deltay)*1
                error -= 1.0
        return line_pixels
    else:
        if p1[1]<p0[1]:
            p = p0
            p0 = p1
            p1 = p
        deltax = p1[0]-p0[0]
        deltay = p1[1]-p0[1]
        if deltay==0:
            return line_pixels
        deltaerr = np.abs(deltax/deltay)
        error = 0.0
        x = p0[0]
        for y in range(p0[1],p1[1]+1):
            line_pixels.append((x,y))
            error += deltaerr
            if error>=0.5:
                x += np.sign(deltax)*1
                error -= 1.0
        return line_pixels

def update_map(position,distance,angle):
    distance+=33
    dx = int(np.floor(distance*np.cos(angle)))
    dy = int(np.floor(distance*np.sin(angle)))
    p1 = (position[0]+dx,position[1]+dy)
    line_pixels = line(position,p1)
    # attempting to draw a line
    for pixel in line_pixels:
        map[pixel[0]][pixel[1]] = 1.0
    # end attempt
    return

def read_log(point=(250,250),filename="log_scan.csv"):
    import pandas as pd
    log = pd.read_csv(filename)
    angle = log[log.columns[0]].values
    angle = angle/18.8*np.pi*2
    distance = log[log.columns[1]].values 
    for i in range(log.size//2):
        update_map(point,distance[i],angle[i])  

    

if __name__ == "__main__":

    read_log(point=(250,250),filename="log_scan.csv")
    read_log(point=(360,250),filename="log_scan1.csv")
    import matplotlib.pyplot as plt
    plt.imshow(map)
    plt.show()
