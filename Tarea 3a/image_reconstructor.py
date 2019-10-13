from PIL import Image
import sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg
np.set_printoptions(threshold=np.inf)

def getVecinos(x,y):
    vecinos=[]
    vecinos.append((x+1,y))
    vecinos.append((x-1,y))
    vecinos.append((x,y+1))
    vecinos.append((x,y-1))
    return vecinos


if __name__ == "__main__":

    entrada=str(sys.argv[1])
    salida=str(sys.argv[2])
    im=Image.open(entrada).convert('RGB')
    sol=Image.open(entrada).convert('RGB')
    arr=np.array(im,dtype='int64')
    solu=np.array(sol,dtype='int64')
    Y=arr.shape[0]
    X=arr.shape[1]


    """
    #nh=1
    ### Las siguientes dos funciones fueron obtenidas del auxiliar 7
    def getK(i,j):
        return j * nh + i

    def getIJ(k):
        i = k % nh
        j = k // nh
        return (i, j)
    ###
    """

    incognitasK=[]
    arregloBlancos=[]
    #arregloBlancos_rowind=np.array()
    #arregloBlancos_colind=np.array()
    #arregloBlancos_data=np.array()

    for x in range(X):
        for y in range(Y):
            if (arr[y][x][0]==255) and (arr[y][x][1]==255) and (arr[y][x][2]==255):
                arregloBlancos.append((y,x))
                #incognitasK.append(getK(y,x))
            #print(y,x)
            #print(arr[y,x,0])
            #print(getK(y,x))
    #print(incognitasK)
    incognitas=len(arregloBlancos)
    #print(incognitas)
    """
    A0=np.zeros((incognitas,incognitas))
    b0=np.zeros((incognitas,))
    A1=np.zeros((incognitas,incognitas))
    b1=np.zeros((incognitas,))
    A2=np.zeros((incognitas,incognitas))
    b2=np.zeros((incognitas,))

    """
    A0_rowind=np.array([],dtype=np.int64)
    A0_colind=np.array([],dtype=np.int64)
    A0_data=np.array([],dtype=np.int64)
    b0=np.zeros((incognitas,))

    A1_rowind=np.array([],dtype=np.int64)
    A1_colind=np.array([],dtype=np.int64)
    A1_data=np.array([],dtype=np.int64)
    b1=np.zeros((incognitas,))

    A2_rowind=np.array([],dtype=np.int64)
    A2_colind=np.array([],dtype=np.int64)
    A2_data=np.array([],dtype=np.int64)
    b2=np.zeros((incognitas,))


    ### Las siguientes dos funciones fueron obtenidas del auxiliar 7
    def getK(i,j):
        return arregloBlancos.index((i,j))

    def getIJ(k):
        return arregloBlancos[k]
    ###

    for pair in arregloBlancos:
        incognitasK.append(getK(pair[0],pair[1]))



    ###Deberemos iterar 3 veces sobre el arreglo para resolver 3 veces la EDP, una para cada color
    ###R
    n=0
    for par in arregloBlancos:
        #print(par)
        #print(n)
        #print("entro!")
        
        i=par[0]
        j=par[1]
        k=getK(i,j)
        # k=1 pasa algo raro
        #print(k)
        
        """
        k_u = getK(i, j+1)
        k_d = getK(i, j-1)
        k_l = getK(i-1, j)
        k_r = getK(i+1, j)
        """
        try:
            k_u = getK(i, j+1)
        except ValueError:
            k_u = np.inf

        try:
            k_d = getK(i, j-1)
        except ValueError:
            k_d = np.inf
        try:
            k_l = getK(i-1, j)
        except ValueError:
            k_l = np.inf

        try:
            k_r = getK(i+1, j)
        except ValueError:
            k_r = np.inf

        #print(k_d)
        """
        if(k==1):
            print("separador")
            print(i)
            print(j)
            print(k_u)
            print(k_d)
            print(k_l)
            print(k_r)
        """

        #print(str(par) + "entro a ")
    #Hay 16 casos distintos, dependiendo de si el pixel toca o no bordes de la imagen
    # y en que lados:
        
        #No toca bordes:
        if(((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l in incognitasK) and(k_r  in incognitasK))):

            n+=1
            """
            A0[k,k_u]=1
            A0[k,k_d]=1
            A0[k,k_l]=1
            A0[k,k_r]=1
            A0[k,k]=-4
            """
            b0[k]=0
            
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            
            #print(str(par) + "entro a centro")
        #U
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):

            
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            
            b0[k]=-(arr[i,j+1,0])
            #print(str(par) + "entro a U")
        #L
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  not in incognitasK) and(k_r  in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i-1,j,0])
            #print(str(par) + "entro a L")
        #D
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j-1,0])
            #print(str(par)+ "entro a D")
        #R
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i+1,j,0])
            #print(str(par) + "entro a R")
        #UL
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i-1,j,0])
            #print(str(par) + "entro a UL")
        #UR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i+1,j,0])
            #print(str(par) + "entro a UR")
        #UD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i,j-1,0])
            #print(str(par)+ "entro a UD")
        #LR
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i-1,j,0])-(arr[i+1,j,0])
            #print(str(par) + "entro a LR")
        #LD
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i-1,j,0])-(arr[i,j-1,0])
            #print(str(par) + "entro a LD")
        #RD
        elif((k_u  in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
             
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i+1,j,0])-(arr[i,j-1,0])
            #print(str(par) + "entro a RD")
        #ULR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_d)
            A0_data=np.append(A0_data,1) 
            
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i-1,j,0])-(arr[i+1,j,0])
            #print(str(par) + "entro a ULR")
        #ULD
        elif((k_u not in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            #r
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_r)
            A0_data=np.append(A0_data,1) 
            
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i-1,j,0])-(arr[i,j-1,0])
            #print(str(par) + "entro a ULD")
        #URD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #l
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_l)
            A0_data=np.append(A0_data,1) 
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i,j+1,0])-(arr[i+1,j,0])-(arr[i,j-1,0])
            #print(str(par) + "entro a URD")
        #LRD
        elif((k_u in incognitasK)and (k_d not in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            
            #u
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,k_u)
            A0_data=np.append(A0_data,1)
            #centro
            A0_rowind=np.append(A0_rowind,k)
            A0_colind=np.append(A0_colind,int(k))
            A0_data=np.append(A0_data,-4)
            b0[k]=-(arr[i-1,j,0])-(arr[i+1,j,0])-(arr[i,j-1,0])
            #print(str(par) + "entro a LRD")

        #print(A)
        #ULRD No puede existir dado que no es posible tener un solo pixel blanco
        #(por condiciones de enunciado)
    #print(A0)
    #print(A0_data.size())
    #print(A0_colind.size())
    #print(A0_rowind.size())
    #assert np.all(A0_colind>=0)
    #assert np.all(A0_rowind>=0)
    #print(A0_colind.astype('int32'))
    A0sparse=sp.coo_matrix((A0_data,(A0_rowind,A0_colind)),shape=(incognitas,incognitas),dtype='int64')
    solve0 = sp.linalg.spsolve(A0sparse, b0)
    #print(A0sparse.toarray())
    #print(A)
    #print(solve)
    #print(A.shape)
    #print(n)

    ##G
    for par in arregloBlancos:
        #print(par)
        #print(n)
        #print("entro!")
        
        i=par[0]
        j=par[1]
        k=getK(i,j)
        # k=1 pasa algo raro
        #print(k)
        
        """
        k_u = getK(i, j+1)
        k_d = getK(i, j-1)
        k_l = getK(i-1, j)
        k_r = getK(i+1, j)
        """
        try:
            k_u = getK(i, j+1)
        except ValueError:
            k_u = np.inf

        try:
            k_d = getK(i, j-1)
        except ValueError:
            k_d = np.inf

        try:
            k_l = getK(i-1, j)
        except ValueError:
            k_l = np.inf

        try:
            k_r = getK(i+1, j)
        except ValueError:
            k_r = np.inf

        #print(k_d)
        """
        if(k==1):
            print("separador")
            print(i)
            print(j)
            print(k_u)
            print(k_d)
            print(k_l)
            print(k_r)
        """

        #print(str(par) + "entro a ")
    #Hay 16 casos distintos, dependiendo de si el pixel toca o no bordes de la imagen
    # y en que lados:

        #No toca bordes:
        if(((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l in incognitasK) and(k_r  in incognitasK))):

            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            
            b1[k]=0
            #print(str(par) + "entro a centro")
        #U
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])
            #print(str(par) + "entro a U")
        #L
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  not in incognitasK) and(k_r  in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
             
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i-1,j,1])
            #print(str(par) + "entro a L")
        #D
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
             
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j-1,1])
            #print(str(par)+ "entro a D")
        #R
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i+1,j,1])
            #print(str(par) + "entro a R")
        #UL
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            
            
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
           
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i-1,j,1])
            #print(str(par) + "entro a UL")
        #UR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i+1,j,1])
            #print(str(par) + "entro a UR")
        #UD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i,j-1,1])
            #print(str(par)+ "entro a UD")
        #LR
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i-1,j,1])-(arr[i+1,j,1])
            #print(str(par) + "entro a LR")
        #LD
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
           
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i-1,j,1])-(arr[i,j-1,1])
            #print(str(par) + "entro a LD")
        #RD
        elif((k_u  in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
            
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
            
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i+1,j,1])-(arr[i,j-1,1])
            #print(str(par) + "entro a RD")
        #ULR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_d)
            A1_data=np.append(A1_data,1) 
            
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i-1,j,1])-(arr[i+1,j,1])
            #print(str(par) + "entro a ULR")
        #ULD
        elif((k_u not in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            
            #r
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_r)
            A1_data=np.append(A1_data,1) 
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i-1,j,1])-(arr[i,j-1,1])
            #print(str(par) + "entro a ULD")
        #URD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
             
            #l
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_l)
            A1_data=np.append(A1_data,1) 
             
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i,j+1,1])-(arr[i+1,j,1])-(arr[i,j-1,1])
            #print(str(par) + "entro a URD")
        #LRD
        elif((k_u in incognitasK)and (k_d not in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            #u
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,k_u)
            A1_data=np.append(A1_data,1)
             
            #centro
            A1_rowind=np.append(A1_rowind,k)
            A1_colind=np.append(A1_colind,int(k))
            A1_data=np.append(A1_data,-4)
            b1[k]=-(arr[i-1,j,1])-(arr[i+1,j,1])-(arr[i,j-1,1])

    A1sparse=sp.coo_matrix((A1_data,(A1_rowind,A1_colind)),shape=(incognitas,incognitas),dtype='int64')
    solve1 = sp.linalg.spsolve(A1sparse, b1)

    #B
    for par in arregloBlancos:
        #print(par)
        #print(n)
        #print("entro!")
        
        i=par[0]
        j=par[1]
        k=getK(i,j)
        # k=1 pasa algo raro
        #print(k)
        
        """
        k_u = getK(i, j+1)
        k_d = getK(i, j-1)
        k_l = getK(i-1, j)
        k_r = getK(i+1, j)
        """
        try:
            k_u = getK(i, j+1)
        except ValueError:
            k_u = np.inf

        try:
            k_d = getK(i, j-1)
        except ValueError:
            k_d = np.inf

        try:
            k_l = getK(i-1, j)
        except ValueError:
            k_l = np.inf

        try:
            k_r = getK(i+1, j)
        except ValueError:
            k_r = np.inf

        #print(k_d)
        """
        if(k==1):
            print("separador")
            print(i)
            print(j)
            print(k_u)
            print(k_d)
            print(k_l)
            print(k_r)
        """

        #print(str(par) + "entro a ")
    #Hay 16 casos distintos, dependiendo de si el pixel toca o no bordes de la imagen
    # y en que lados:

        #No toca bordes:
        if(((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l in incognitasK) and(k_r  in incognitasK))):

            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=0
            #print(str(par) + "entro a centro")
        #U
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])
            #print(str(par) + "entro a U")
        #L
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  not in incognitasK) and(k_r  in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i-1,j,2])
            #print(str(par) + "entro a L")
        #D
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j-1,2])
            #print(str(par)+ "entro a D")
        #R
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i+1,j,2])
            #print(str(par) + "entro a R")
        #UL
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i-1,j,2])
            #print(str(par) + "entro a UL")
        #UR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i+1,j,2])
            #print(str(par) + "entro a UR")
        #UD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r  in incognitasK)):
            
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i,j-1,2])
            #print(str(par)+ "entro a UD")
        #LR
        elif((k_u  in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
            
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i-1,j,2])-(arr[i+1,j,2])
            #print(str(par) + "entro a LR")
        #LD
        elif((k_u  in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
             
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i-1,j,2])-(arr[i,j-1,2])
            #print(str(par) + "entro a LD")
        #RD
        elif((k_u  in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
             
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
             
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i+1,j,2])-(arr[i,j-1,2])
            #print(str(par) + "entro a RD")
        #ULR
        elif((k_u not in incognitasK)and (k_d  in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            
            #d
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_d)
            A2_data=np.append(A2_data,1) 
             
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i-1,j,2])-(arr[i+1,j,2])
            #print(str(par) + "entro a ULR")
        #ULD
        elif((k_u not in incognitasK)and (k_d  not in incognitasK) and(k_l not in incognitasK) and(k_r in incognitasK)):
            
            #r
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_r)
            A2_data=np.append(A2_data,1) 
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i-1,j,2])-(arr[i,j-1,2])
            #print(str(par) + "entro a ULD")
        #URD
        elif((k_u not in incognitasK)and (k_d not in incognitasK) and(k_l  in incognitasK) and(k_r not in incognitasK)):
            
            #l
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_l)
            A2_data=np.append(A2_data,1) 
             
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i,j+1,2])-(arr[i+1,j,2])-(arr[i,j-1,2])
            #print(str(par) + "entro a URD")
        #LRD
        elif((k_u in incognitasK)and (k_d not in incognitasK) and(k_l not in incognitasK) and(k_r not in incognitasK)):
            #u
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,k_u)
            A2_data=np.append(A2_data,1)
            
            #centro
            A2_rowind=np.append(A2_rowind,k)
            A2_colind=np.append(A2_colind,int(k))
            A2_data=np.append(A2_data,-4)
            b2[k]=-(arr[i-1,j,2])-(arr[i+1,j,2])-(arr[i,j-1,2])

    A2sparse=sp.coo_matrix((A2_data,(A2_rowind,A2_colind)),shape=(incognitas,incognitas),dtype='int64')
    solve2 = sp.linalg.spsolve(A2sparse, b2)
    #print(solve0)


    #print(solve1)
    #print(solve2)

    for par in arregloBlancos:
        k=getK(par[0],par[1])
        solu[par[0],par[1],0]=solve0[k]
        solu[par[0],par[1],1]=solve1[k]
        solu[par[0],par[1],2]=solve2[k]


    sol=Image.fromarray(solu.astype('uint8'))
    sol.save(salida)
      
        

    #print(len(arregloBlancos))
    #print(arregloBlancos)

    #print(getVecinos(arregloBlancos[0][0],arregloBlancos[0][1]))
    #print(X,Y)
    #print(arr.shape)
    #print(arr[0][0])

