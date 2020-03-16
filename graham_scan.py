import cv2
import numpy as np
import traceback


class ConvexHull:
    def __init__(self, max_span = 500, num_points = 25):
        self.show_process = False
        self.span = max_span
        self.blank = np.zeros(shape = (self.span,self.span,3),dtype = np.uint8)
        self.blank2 = self.blank.copy()
        self.blank3 = self.blank.copy()
        self.num_points = num_points
        self.points = np.random.randint(20,self.span-50,size = (self.num_points,2))
        self.bottom_point = None
        self.other_points = None
        self.sorted_points = None
        self.hull_points = None
        self.final_hull_points = None
        self.draw_points = True

    def orientation(self, p1,p2,p3):
        return   (p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])

    def separate_pivot_from_rest(self):
        max_arg = np.argmax(self.points[:,1])
        other_indices = [True,]*len(self.points)
        other_indices[max_arg] = False

        self.bottom_point = self.points[max_arg]
        self.other_points = self.points[other_indices]

    def do_polar_sort(self):
        thetas = np.arctan2((self.bottom_point[1]-self.other_points[:,1]),(self.bottom_point[0]-self.other_points[:,0]))
        sorted_args = np.argsort(thetas)
        sorted_thetas = thetas[sorted_args][::-1]
        self.sorted_points = self.other_points[sorted_args][::-1]
        if self.draw_points:
            cv2.circle(self.blank2,(tuple(self.bottom_point)),5,(255,0,0),-1)
            for i,point in enumerate(self.sorted_points):
                cv2.circle(self.blank2,(point[0],point[1]),2,(0,0,255),-1)



    def scan(self):
        self.hull_points =[np.asarray(self.bottom_point),self.sorted_points[0]]
        i=1 
        while(i<len(self.sorted_points)):            
            dirr = self.orientation(self.hull_points[-2],self.hull_points[-1],self.sorted_points[i])
            if dirr<0:
                self.hull_points.append(self.sorted_points[i])
                
            elif dirr>0:
                del self.hull_points[-1]
                self.hull_points.append(self.sorted_points[i])
                concave = True
                while(concave and len(self.hull_points)>2):     
                    dirr2 = self.orientation(self.hull_points[-3],self.hull_points[-2],self.hull_points[-1])
                    if dirr2>0:
                        del self.hull_points[-2]
                    else:
                        concave = False                
            else:
                pass

            i+=1

        self.final_hull_points =  self.hull_points = [i.tolist() for i in self.hull_points]
        self.hull_points.append(self.hull_points[0])


    def run_graham_scan(self,viz = True):
        self.separate_pivot_from_rest()
        self.do_polar_sort()
        self.scan()
        if viz:
            i=0
            try:
                while(i<len(self.hull_points)-1):
                    p1,p2 = self.hull_points[i], self.hull_points[i+1]
                    cv2.line(self.blank2,(p1[0],p1[1]),(p2[0],p2[1]),(0,255,0),1,1)
                    cv2.imshow("img",self.blank2)
                    cv2.waitKey(50)
                    i+=1
                cv2.waitKey(0)
            except:
                traceback.print_exc()
            cv2.destroyAllWindows()




if __name__ == '__main__':
    conv = ConvexHull(max_span = 600, num_points = 100)
    conv.run_graham_scan()