"""
@author: Michal Smid, HZDR 2020
Rosahami_processor

Rossendorfer
  Saxs
    HAPG
      Mirror
"""

from mmpxrt import mmpxrt
import pickle
import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import sys
import math
import time
import os
import matplotlib.pyplot as plt
import math
from scipy import interpolate
from matplotlib.patches import Ellipse
import scipy.signal
import rossendorfer_farbenliste as rofl
import matplotlib
from scipy.interpolate import griddata

import warnings
warnings.filterwarnings("ignore")
global times, time_labels
times =[]
time_labels =[]

def version():
    print('Rosahami processor, 1.0.5  (31.8.2022)')
    print('Rossendorfer SAXS HAPG mirror.')
    print('Michal Smid, HZDR')


def run_simulation(p):
    p['source']['continuumAdd']=True
    p['source']['continuumMarks']=False
    p['source']['continuumAddedRatio']=0.
    p['source']['divergenceAutomatic']=True
    p['simulation']['collectLostBeams']=False

    if p['simulation']['numraysE']>0:
        p['simulation']['numraysB']=round(10**(p['simulation']['numraysE']))
        p['simulation']['numraysM']=round(10**(p['simulation']['numraysE']-1))


    p=mmpxrt.geometry(p)
    sim=p['simulation']
    s=p['source']
    sg=p['sg']
    nump=sim['num_processes'];

    s['rOffset']=[0,0,0]
    sg['windowX']=10
    sg['windowY']=10
    start = time.time()
    s['showrealspatial']=False
    s['continuum']=False
    s['rOffsetRatio']=0.
    s['rOffset']=[0,0,0]
    divRing=s['divergenceRing']

    ## Flat run
    print( '\nGoing to raytrace (monochromatic, flat)')
    sg['numrays']=p['simulation']['numraysM']
    s['divergenceRing']=0
    if nump>1:
        sg['numrays']=int(np.round(p['simulation']['numraysM']/nump))
        monorrr = mmpxrt.raytrace_multiprocess(p,nump)
    else:
        monorrr = mmpxrt.raytrace(p,None,None)


    ## Ring run
    print( '\nGoing to raytrace (ring)')
    s['divergenceRing']=divRing
    s['divergenceRectangular']=False;
    sg['numrays']=p['simulation']['numraysR']
    sg['numraysR']=p['simulation']['numraysR']
    if nump>1:
        sg['numrays']=int(np.round(sg['numraysR']/nump))
        ringrrr = mmpxrt.raytrace_multiprocess(p,nump)
    else:
        ringrrr = mmpxrt.raytrace(p,None,None)

    print(' ')
    end = time.time()

    spectrorrr={}
    spectrorrr['elapsedTime']=end-start
    spectrorrr['mono']=monorrr
    spectrorrr['ring']=ringrrr

    fn=p['simulation']['out_data_directory']  +'mmpxrt_results_' +p['simulation']['name']
    pickle.dump( spectrorrr, open( fn, "wb" ) )
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )

    return spectrorrr


def run_SAXS_simulation(p):
    p['source']['continuumAdd']=True
    p['source']['continuumMarks']=False
    p['source']['continuumAddedRatio']=0.
    p['source']['divergenceAutomatic']=True
    p['simulation']['collectLostBeams']=False

    if p['simulation']['numraysE']>0:
        p['simulation']['numraysB']=round(10**(p['simulation']['numraysE']))
        p['simulation']['numraysM']=round(10**(p['simulation']['numraysE']-1))


    p=mmpxrt.geometry(p)
    sim=p['simulation']
    s=p['source']
    sg=p['sg']
    nump=sim['num_processes'];

    s['rOffset']=[0,0,0]
    sg['windowX']=10
    sg['windowY']=10
    start = time.time()
    s['showrealspatial']=False
    s['continuum']=False
    s['rOffsetRatio']=0.
    s['rOffset']=[0,0,0]
    divRing=s['divergenceRing']

    ## SAXS run
    print( '\nGoing to raytrace (ring)')
    s['divergenceRing']=divRing
    s['divergenceRectangular']=False;
    sg['numrays']=p['simulation']['numraysR']
    sg['numraysR']=p['simulation']['numraysR']
    if nump>1:
        sg['numrays']=int(np.round(sg['numraysR']/nump))
        ringrrr = mmpxrt.raytrace_multiprocess(p,nump)
    else:
        ringrrr = mmpxrt.raytrace(p,None,None)

    print(' ')
    end = time.time()

    spectrorrr={}
    spectrorrr['elapsedTime']=end-start
    spectrorrr['ring']=ringrrr

    fn=p['simulation']['out_data_directory']  +'mmpxrt_results_' +p['simulation']['name']
    pickle.dump( spectrorrr, open( fn, "wb" ) )
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )

    return spectrorrr    
    
# %%##############################################################################
def evaluate_simulation(p,spectrorrr,quarterring,climmax):
    so=p['source']
    c=p['crystal']
    sg=p['sg']
    mono_rrr=spectrorrr['mono']
    ring_rrr=spectrorrr['ring']

    elapsedTime=spectrorrr['elapsedTime']
    evalu={}
    p['evalu']=evalu
    ev=p['evalu']

    fig= plt.figure(figsize=(16,7))

    nl='\n'
    s=' \t'

    ii=r''
    ii=ii+ '$\mathcal{'+ p['simulation']['name'] +'}$'+ nl
    ii=ii +p['simulation']['comment']+ nl+nl
    ii=ii +'central E:  {:2.0f}'.format(so['EcentralRay'])+  ' eV '+ nl
    ii=ii +'number of rays:   {:2.0e} + {:2.0e}'.format(ring_rrr['numrays'],mono_rrr['numrays']) + nl
    if (elapsedTime>300):
        ii=ii +'time:  {:2.0f} min., {:2.0f} r/s'.format(elapsedTime/60,(mono_rrr['numrays'])/elapsedTime) + nl
    else:
        ii=ii +'time:  {:2.0f} s,  {:2.0f} r/s'.format(elapsedTime,(mono_rrr['numrays'])/elapsedTime) + nl
    ii=ii +nl+'$\mathtt{Geometry}$' +nl
    ii=ii+ '$d_{{{{SC}}}}$:  {:2.2f}'.format(sg['Edist'])+ ' mm'+ nl
    ii=ii+ '$d_{{{{CD}}}}$:  {:2.2f}'.format(sg['Edist_dect'])+ ' mm' +nl
    ii=ii +'$\\theta_{{{{Bragg}}}}$:  {:2.2f}'.format(sg['ThBragg']/np.pi*180) +'$^\\circ$' +nl
    ii=ii +'gap between crystals:  {:2.0f} mm'.format(p['crystal']['gap']) +nl
#    ii=ii +'ring $2\\theta$: \t {:2.4f} °'.format(p['source']['divergenceRing']/np.pi*180) +nl

    ii=ii+ nl

    mmpxrt.evaluateMono(p,mono_rrr)


    ax = fig.add_subplot(131)
    plt.title('Rings')

    l=p['geometry']['CrystalSource']+p['geometry']['CrystalDetector']
    if np.size(so['divergenceRing'])==1:
        r=np.sin(so['divergenceRing'])*l
        circle1 = plt.Circle((0, 0), r*1.05, linewidth=0.5,color=[0.7,0,0],fill=False)
        ax.add_artist(circle1)
    drawDet(p,ring_rrr,ax,-1,-1)
    if quarterring:
        plt.title('Detected 1/4 ring (on 100um pixels)')
        plt.xlim(0,9)
        plt.ylim(0,12)



    ax = fig.add_subplot(132)
    plt.title('Isotropic')

    l=p['geometry']['CrystalSource']+p['geometry']['CrystalDetector']
    drawDet(p,mono_rrr,ax,-1,-1)



#getting efficiency from ring simulation
    ## efficiency
    rrr=ring_rrr
    reflectedratio=rrr['effdet']/rrr['effcnt']
    efficiency=reflectedratio
    p['evalu']['efficiency']=efficiency


    ii=ii+ nl
    rOff=np.linalg.norm(so['rOffset'])

    if c['mosaicity']==0:
        c['crystalPeakReflectivity']=c['crystalIntegratedReflectivity']/c['rockingCurveFWHM']

    totalEfficiency=p['evalu']['efficiency']*c['crystalPeakReflectivity']

    ii=ii +nl+ 'efficiency of given ring:  {:2.1f} \%'.format(totalEfficiency*100)



    # print info
    from matplotlib import rc
    ax = fig.add_subplot(133)
#    t=plt.text(-0.1,1,ii,transform=ax.transAxes,fontsize=12,VerticalAlignment='top')
#    t=plt.text(-0.1,1,ii,transform=ax.transAxes,VerticalAlignment='top')
 #   t=plt.text(-0.1,1,ii)
    ax.axis('off')
    ax.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    plt.savefig('mmpxrt_' +p['simulation']['name']+'.png' , bbox_inches ='tight',dpi=140)
    fn=p['simulation']['out_data_directory']  +'mmpxrt_parameters_' +p['simulation']['name']
    pickle.dump( p, open( fn, "wb" ) )
    return totalEfficiency



# %%##############################################################################
def drawDet(p,rrr,ax,pxsize,climmax):
    colores=rrr['colores']
    rayres=rrr['rayres']
    E0s=rrr['E0s']
    ev=p['evalu']
    Sdetector=p['sg']['Sdetector']

    numrays=np.size(colores)
    posCont=np.full((numrays,2),np.nan)
    posR=np.full((numrays,2),np.nan)
    posG=np.full((numrays,2),np.nan)
    posB=np.full((numrays,2),np.nan)
    posCont=np.full((numrays,2),np.nan)
    posAll=np.full((numrays,2),np.nan)
    po=np.array([0.,0.],float)
    for i in np.arange(np.shape(rayres)[0]):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)#distance from detector center
          posAll[i,:]=[absPos[1], absPos[0]]
          if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
             po[1]=po[1]*-1
          posAll[i,:]=po

          if colores[i]==1:
              posR[i,:]=po
          else:
              if colores[i]==2:
                  posG[i,:]=po
              else:
                  if colores[i]==3:
                      posB[i,:]=po
          if colores[i]==4:
            posCont[i,:]=po

    if (np.nansum(np.nansum(posR))==0):
        return

    ## get the optimal ranges
    pC=posR
    xs=np.abs(pC[:,0])
    ys=np.abs(pC[:,1])
    xs2=xs[np.logical_not(np.isnan(xs))]
    ys2=ys[np.logical_not(np.isnan(ys))]
    windowX=np.quantile(xs2,0.95)*1.1
    windowY=np.quantile(ys2,0.95)*1.1

    if p['geometry']['detectorWidth']>0:
        windowX=p['geometry']['detectorWidth']/2


    cnt=np.shape(posCont)[0]
    if p['simulation']['PSFWindowY']>-1:
        windowY=p['simulation']['PSFWindowY']
    if p['simulation']['PSFStepY']>-1:
        stepY=p['simulation']['PSFStepY']
    if p['simulation']['PSFWindowX']>-1:
        windowX=p['simulation']['PSFWindowX']
    if pxsize>0:
        stepX=pxsize
        stepY=pxsize
        windowX=10
        windowY=windowX*0.6
        #aspe='equal'
        aspe='auto'
    else:
        stepX=1
        stepY=0.5
        aspe='auto'
    ## plt.plotting
    cntrsX=np.arange(-1*windowX,windowX,stepX)
    cntrsY=np.arange(-1*windowY,windowY,stepY)

    edX=cntrsX+stepX/2
    edY=cntrsY+stepY/2
    #cntrs=[cntrsX,cntrsY]
    eds=[edX,edY]
    pos=posAll
    nR = np.histogram2d(pos[:,0],pos[:,1],eds)[0]
    if np.size(nR)==0:
        print("There is nothing reaching the detector, I'm failing.")
        return
        
    nR[0,0]=0
    nR[np.shape(nR)[0]-1,np.shape(nR)[1]-1]=0
    nR[0,np.shape(nR)[1]-1]=0
    nR[np.shape(nR)[0]-1,0]=0
    nR2=np.flip(nR,1)
    #nR2=np.transpose(nR)
    plt.imshow(nR2,extent=(windowY,-1*windowY,windowX,-1*windowX),aspect=aspe,origin='lower')


    ## profiles

    su2=np.sum(nR,0)
    su2y=np.sum(nR,1)
    su2[0]=0
    su2[np.size(su2)-1]=0
    su2y[0]=0
    su2y[np.size(su2y)-1]=0

    su2=su2/np.max(su2)*0.5*windowX-windowX
    su2y=su2y/np.max(su2y)*0.5*windowY-windowY

#    plt.plot(cntrsY,np.append(np.nan,su2),'w',linewidth=1)
 #   plt.plot(np.append(np.nan,su2y),cntrsX,'w',linewidth=1)

    #selected profile
    evalSelectY=p['geometry']['evaluation_width']
    es2=evalSelectY/2*1e3
    wy=windowY*1e3*1.1

    vyy=np.squeeze(np.asarray(p['evalu']['verticalSelectPSF'][1,:]))
    vyy=(vyy/np.nanmax(vyy)*0.5*windowX-windowX)*1e3

    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    #plt.colorbar()
    if climmax>0:
        plt.clim(0,climmax)
#    plt.xlim(0,windowY)
 #   plt.ylim(-1*windowX,0)




# %%##############################################################################
def make_unwrap_map(rrr,p,map_width,map_height,map_resolution):
    rayres=rrr['rayres']
    ThBragg=np.arcsin(12398/p['source']['EcentralRay']/p['crystal']['d2'])

    #calculating the angles alpha X and Y from rayres
    dx=(rayres[:,1,0]-rayres[:,0,0])
    dy=(rayres[:,1,1]-rayres[:,0,1])
    dz=(rayres[:,1,2]-rayres[:,0,2])
    dxz=(dx**2+dy**2)**0.5
    alZ=np.arctan(dz/dx)+ThBragg
    alY=np.arctan(dy/dxz)
    al=(alZ**2+alY**2)**0.5
    phi=np.arctan2(alY,alZ)

    #getting position on the detector
    colores=rrr['colores']
    E0s=rrr['E0s']
    ev=p['evalu']
    Sdetector=p['sg']['Sdetector']

    numrays=np.size(colores)
    pos=np.full((numrays,2),np.nan)    #arracy containing positions of each ray on detector
    po=np.array([0.,0.],float)
    for i in np.arange(np.shape(rayres)[0]):
          absPos=rayres[i,2,:]
       #projection
          po[0]=absPos[1]#y in 3D becomes x in 2D
          po[1]=((absPos[0]-Sdetector[0])**2 + (absPos[2]-Sdetector[2])**2) ** (1/2)#distance from detector center
          if (absPos[0]-Sdetector[0])<0:#see if it was 'front' or 'behind' the detector
             po[1]=po[1]*-1
          pos[i,:]=po

    # %% make the Alpha maps

    ys=pos[:,0]
    ds=pos[:,1]
    pxsize=map_resolution
    wD=map_width/2
    wY=map_height
    detD=np.arange(-wD,wD,pxsize)
    detY=np.arange(-0,wY,pxsize)
    cnts=np.zeros((np.size(detY),np.size(detD)))
    alZmap=np.zeros((np.size(detY),np.size(detD)))
    alYmap=np.zeros((np.size(detY),np.size(detD)))
    ays=np.abs(ys)
    print("Making an unwrap map.")
    print("distance d running from {:2.2f} till {:2.2f} mm with step {:2.2f} mm".format(-wD,wD,pxsize))
    for di,d in enumerate(detD):
        print("d = {:2.2f} mm".format((d)))
        for yi,y in enumerate(detY):  #going throug each pixel of the map
            #finding all rays hitting this pixel:
            pxd=np.logical_and(ds>d,ds<(d+pxsize))
            pxy=np.logical_and(ays>y,ays<(y+pxsize))
            pxc=np.logical_and(pxd,pxy)

            cnts[yi,di]=np.sum(pxc) #number of such rays
            if cnts[yi,di]>0:
                alZmap[yi,di]=np.nanmean(alZ[pxc]) #getting the mean alpha values
                alYmap[yi,di]=np.nanmean(np.abs((alY[pxc])))

    ## saving the map for further use:
    D,Y=np.meshgrid(detD,detY)
    name=p['simulation']['name']
    t={}
    t['D']=D
    t['Y']=Y
    t['alYmap']=alYmap
    t['alZmap']=alZmap
    t2={}
    t2['cnts']=cnts
    t2['detY']=detY
    t2['detD']=detD
    t2['wD']=wD
    t2['wY']=wY
    t2['name']=name
    pickle.dump( t, open( "rosahami-unwrap-map-"+name+".pickle", "wb" ) )


    # %% just drawing : those take huuuge time
    if 0:
        fig= plt.figure(figsize=(16,7))
        plt.subplot(121)
        plt.scatter(pos[:,0],pos[:,1],c=phi,s=15)
        plt.title('phi of emerging beam')
        plt.colorbar()
        plt.subplot(122)
        plt.scatter(pos[:,0],pos[:,1],c=al,s=15)
        plt.title('absolute divergence of emerging beam')
        plt.colorbar()
        plt.savefig('mmpxrt_unwrap1.png' , bbox_inches ='tight',dpi=140)

    # %% showing the phi-phid dependence
    if 0:
        fig= plt.figure(figsize=(16,7))
        phid=np.arctan2(pos[:,0],pos[:,1])
        pih=np.pi/2
        plt.plot(np.abs(phi),np.abs(phid),'k.',markersize=0.5)
        plt.grid()
        #polynomial: bad
        nonnan=np.invert(np.isnan(phi))
        train_x=np.abs(phi[nonnan])
        train_y=np.abs(phid[nonnan])
        pf=np.polyfit(train_x,train_y,3)
        x=np.arange(0,np.pi,0.1)
        y=np.polyval(pf,x)
        step=0.01
        window=0.2
        gr=np.arange(0,np.pi,step)
        gry=gr*0
        for i,x in enumerate(gr):
            rang=np.logical_and((train_x>(x-window)),(train_x<(x+window)))
            pf=np.polyfit(train_x[rang],train_y[rang],3)
            gry[i]=np.polyval(pf,x)
        plt.plot(gr,gry,'r-')
        plt.xlabel('phi - emitted [rad]')
        plt.ylabel('phi - detected [rad]')
        plt.savefig('mmpxrt_unwrap_phimap.png' , bbox_inches ='tight',dpi=140)

    # %% graph showign of linearity in phi -> it is not linear
    if 0:
        rdt=180/np.pi
        w=0.2
        sel1=(phi>45/rdt) * (phi<(45+w)/rdt)
        sel2=(phi>30/rdt) * (phi<(30+w)/rdt)
        sel3=(phi>60/rdt) * (phi<(60+w)/rdt)
        sel4=(phi>15/rdt) * (phi<(15+w)/rdt)
        sel5=(phi>75/rdt) * (phi<(75+w)/rdt)
        sel=sel1+sel2+sel3+sel4+sel5
        fig= plt.figure(figsize=(19,7))
        plt.subplot(121)
        plt.plot(pos[sel,0],pos[sel,1],'r*',markersize=0.2)
        plt.title('phi of emerging beam')
        plt.grid()
        l=70
        phs=np.array([15,30,45,60,75])/rdt
        phd=np.interp(phs,gr,gry)
        for ph in phd:
            plt.plot([0,np.sin(ph)*l],[0,np.cos(ph)*l],'k',linewidth=0.5)
        plt.xlim([0,55])
        plt.ylim([0,12])
        plt.savefig('mmpxrt_unwrap2.png' , bbox_inches ='tight',dpi=140)
    return t,t2


# %%##############################################################################
#def unwrap_map_pictures(cnts,alYmap,valid,detY,yp,xp,alZmap,zp,detD,wD,wY,name):
def unwrap_map_pictures(t,t2,E0):
    ## % MAKING THE MODEL::: subtracting the linear thingy
    alYmap=t['alYmap']
    alZmap=t['alZmap']
    detY=t2['detY']
    detD=t2['detD']
    cnts=t2['cnts']
    detY=t2['detY']
    detD=t2['detD']
    wD=t2['wD']
    wY=t2['wY']
    name=t2['name']

    valid=cnts>5

    alYmap[np.invert(valid)]=np.nan
    yp=np.nanmean(alYmap,1)
    xp=np.arange(np.size(yp))
    sel=np.isfinite(yp)
    p=np.polyfit(xp[sel],yp[sel],1)
    ypf=np.polyval(p,xp)
    on=np.ones(np.shape(alYmap)[1])
    alYmodel=np.matmul(np.transpose(np.matrix(ypf)),np.matrix(on))

    prY=np.polyfit(detY[sel],yp[sel]*1e3,1)  #fit in real units

    alZmap[np.invert(valid)]=np.nan
    zp=np.nanmean(alZmap,0)
    xp=np.arange(np.size(zp))
    sel=np.isfinite(zp)
    quadratic=0

    lambd=12398/E0/10 #nm
    qc=2*np.pi/lambd #conversion between divergence angle alpha=2theta[mrad] and q [nm-1]
    print(qc)

    if quadratic:#fitting: quadratic
        p=np.polyfit(xp[sel],zp[sel],2)
        prX=np.polyfit(detD[sel],zp[sel]*1e3,2)  #fint in real units
    else:
        p=np.polyfit(xp[sel],zp[sel],1)
        prX=np.polyfit(detD[sel],zp[sel]*1e3,1)  #fint in real units

    zpf=np.polyval(p,xp)

    # %

    fig, axs  = plt.subplots(1, 3, sharey='row',figsize=(18,8))

    plt.axes(axs[0])#################################################################

    plt.imshow(alYmap*1e3,extent=(-wD,wD,wY,0),cmap=rofl.cmap())
    prof=alYmap[:,int(np.shape(alYmap)[1]/2)]
    plt.plot(prof*500,detY,'w')
    plt.title('2Theta Y [mrad]  (E_xfel= {:.0f} eV'.format(E0))
    plt.xlabel('detector X [mm]')

    #plt.xlabel('detector X [mm]')
    plt.ylabel('detector Y [mm]')
    plt.plot(ypf*500,detY,'r',linewidth=1)
    plt.text(-10,2,'2Th_Y ~ {:.3f} y '.format(prY[0]),fontsize=14,color='w')
    plt.text(-10,5,'q_y [nm-1] ~= {:.4f} y [mm]'.format(prY[0]/qc),fontsize=14,color='w')


    plt.axes(axs[1])#################################################################
    plt.title('2Theta X [mrad]')
    if quadratic:
        plt.text(-10,2,'2Th_X ~ {:.3f} x + {:.3f} x^2'.format(prX[1],prX[0]),fontsize=14,color='w')
        plt.text(-10,5,'aspect change ~ {:.3f} '.format(prY[0]/prX[1]),fontsize=14,color='w')
    else:
        plt.text(-10,2,'2Th_X ~ {:.3f} x'.format(prX[0]),fontsize=14,color='w')
        plt.text(-10,5,'aspect change ~ {:.3f} '.format(prY[0]/prX[0]),fontsize=14,color='w')
        plt.text(-10,7,'q_x [nm-1] ~= {:.4f} x [mm]'.format(prX[0]/qc),fontsize=14,color='w')


    plt.imshow(alZmap*1e3,extent=(-wD,wD,wY,0),cmap=rofl.cmap())
    prof=alZmap[int(np.shape(alZmap)[0]/2),:]
    plt.plot(detD,prof*500+wY/2,color=[0.5,0.5,0.5]) #plotting the first line
    plt.xlabel('detector X [mm]')


    plt.plot(detD,zpf*500+wY/2,'r',linewidth=1)
    plt.plot(detD,detD*0+wY/2,'k',linewidth=1)


    on=np.ones(np.shape(alYmap)[0])
    alZmodel=np.matmul(np.transpose(np.matrix(on)),np.matrix(zpf))


    plt.axes(axs[2])
    alDev=np.power( (np.power(alZmap-alZmodel,2)+ np.power(alYmap-alYmodel,2)) , 0.5)
 #   alAmap=np.power( (np.power(alYmap,2)+ np.power(alZmap,2)) , 0.5)

    plt.imshow(alDev*1e3,extent=(-wD,wD,wY,0),cmap=rofl.cmap())
    plt.title('deviation [mrad]')
    if quadratic:
        plt.clim(0,0.2)
    else:
        plt.clim(0,0.7)
    plt.colorbar()
    plt.xlabel('detector X [mm]')


    plt.savefig('mmpxrt_unwrapmap_'+name+'_quadratic.png' , bbox_inches ='tight',dpi=140)


    if 0:# %% paper picture
        fig, axs  = plt.subplots(1, 1, sharey='row',figsize=(6,5))

        plt.title(r'2$\theta$[mrad]')

        plt.imshow(alZmap*1e3,extent=(-wD,wD,wY,0),cmap=rofl.cmap())
        prof=alZmap[int(np.shape(alZmap)[0]/2),:]


        alDev=np.power( (np.power(alZmap-alZmodel,2)+ np.power(alYmap-alYmodel,2)) , 0.5)
    #    alAmap=np.power( (np.power(alYmap,2)+ np.power(alZmap,2)) , 0.5)

        plt.imshow(alDev*1e3,extent=(-wD,wD,wY,0),cmap=rofl.cmap())
        plt.title('absolute deviation [mrad]')
        plt.xlabel('detector x [mm]')
        plt.ylabel('detector y [mm]')

        plt.colorbar()




        plt.savefig('mmpxrt_unwrapmap_'+name+'_paperc.png' , bbox_inches ='tight',dpi=300)


# %%##############################################################################
def remove_jungfrau_stripes(im):
    im[512:523,:]=im[512:523,:]/2
    im[:,511:513]=im[:,511:513]/2
    im[255:257,:]=im[255:257,:]/2
    im[:,255:257]=im[:,255:257]/2
    return im

def load_unwrap_map(name):
    """
    Returns:
          2D interpolated functions, to those functions you passes the X and Y
          coordinates of pixel, and it will return you either the horizontal
          or vertical scattering angle.
    """
    t=pickle.load(open( "rosahami-unwrap-map-"+name+".pickle", "rb" ) )

    X=t['D'] #D & Y are the cordinates on detector [mm] (D is the 'horizontal')
    Y=t['Y']
    alX=t['alZmap'] #alpha X and alpha Y are the angle between each ray and central ray
    alY=t['alYmap']
    alX[np.isnan(alX)]=0
    alY[np.isnan(alY)]=0

    interpAlX = interpolate.RectBivariateSpline(X[1,:],Y[:,1],np.transpose(alX),kx=1,ky=1)
    interpAlY = interpolate.RectBivariateSpline(X[1,:],Y[:,1],np.transpose(alY),kx=1,ky=1)

    return interpAlX,interpAlY


###############################################################################
def do_radial_average(alRange,points,sel,column = 2):
    """ Performs the radial average of the data

    Parameters:
         alRange : array of scattering angles to which I want to integrate
         points : the big points field
         sel : boolean array - selection from which region to integrate
         column : from which column of points to taka data

     Returns:
         sig : the radial average
    """
    sig=np.zeros(np.size(alRange))
    da=alRange[1]-alRange[0]
    for ai,a in enumerate(alRange):
        selA=np.logical_and(points[3,:]>=a,points[3,:]<(a+da))
        selF=np.logical_and(sel,selA)
        sig[ai]=np.nanmean(points[column,selF])
    return sig


###############################################################################
def make_radial_scattering_old(alRange,sigdown,sigup=[],points=[]):
    if sigup==[]:
        sigup=sigdown
    nump=np.shape(points)[1]
    ram = np.zeros(nump)
    for ii in np.arange(nump-2):
        r=points[3,ii]
        if points[1,ii]>0:
            ff=np.interp(r,alRange,sigdown)
        else:
            ff=np.interp(r,alRange,sigup)
        ram[ii]=ff
    return ram

def make_radial_scattering(alRange,sigdown,sigup=[],points=[]):
 #  faster version of make_radial_scattering
#    ram = np.zeros(nump)
    r=points[3,:]
    if sigup==[]:
        ff=np.interp(r,alRange,sigdown)
    else:
#        upsel=points[1,:]>0
        downsel=points[1,:]>0
        ffup=np.interp(r,alRange,sigup)
        ffdown=np.interp(r,alRange,sigdown)
        ff=ffup
        ff[downsel]=ffdown[downsel]
    return ff


def do_unwrap_old(im,p,interpAlX,interpAlY):
    """Converts the detected image to scattered angles X & Y

    Parameters:
        im : the pixeled data of the experimental data
        p : Dictionary of input parameters.
        interpAlX,interpAlY : the interpolated map

    Returns:
        points: double[10,number of pixels]
         -each row in corresponds to one pixel of original data
         - columns as follows:
         0 alX
         1 alY
         2 plpltintensity
         3 alR
         -remaining columns are free for further use

    """
    print('-- Do unwrap.')

    xs=(np.arange(np.shape(im)[1])-p['rough_center_x'])*p['pxsize']
    ys=(np.arange(np.shape(im)[0])-p['rough_center_y'])*p['pxsize']

    points=np.zeros((10,np.size(xs)*np.size(ys)))

    i=0
    #mapping: going through each detected pixel, assigning an alpha angles to it
    xoff=p['xoff_um']/1000
    yoff=p['yoff_um']/1000
    halfwidth_mm=p['halfwidth_mm']
    halfheight_mm=p['halfheight_mm']
    xstretch=p['xstretch']
    ystretch=p['ystretch']
    for xi,x in enumerate(xs):
        for yi,y in enumerate(ys):
            if np.abs(x)>halfwidth_mm:
                continue
            if np.abs(y)>halfheight_mm:
                continue

            #correction for crystal offset
            x2=x
            if p['horizontal_crystal_offset']!=0:
                if y<0:
                    x2=x2+p['horizontal_crystal_offset']
            aX=interpAlX((x2-xoff)*xstretch/100,np.abs(y-yoff)*ystretch/100)
            aY=interpAlY((x2-xoff)*xstretch/100,np.abs(y-yoff)*ystretch/100)
            if y<0:
                aY=aY*-1
            aR=(aX**2 + aY**2 )**0.5
            points[:,i]=(aX,aY,im[yi,xi],aR,0,0,0,0,0,0)
            i=i+1
            if np.mod(i,20000)==0:
                print("{:.0f} ".format(np.round(i/1e4)), end="")

    points=points[:,1:i]
    return points

def do_unwrap(im,p,interpAlX,interpAlY):
    """Converts the detected image to scattered angles X & Y
    Trying to be faster then older do_unwrap

    Parameters:
        im : the pixeled data of the experimental data
        p : Dictionary of input parameters.
        interpAlX,interpAlY : the interpolated map

    Returns:
        points: double[10,number of pixels]
         -each row in corresponds to one pixel of original data
         - columns as follows:
         0 alX
         1 alY
         2 plpltintensity
         3 alR
         -remaining columns are free for further use

    """

    xs=(np.arange(np.shape(im)[1])-p['rough_center_x'])*p['pxsize']  #rough coordinates of all pixels in JF[ mm]
    ys=(np.arange(np.shape(im)[0])-p['rough_center_y'])*p['pxsize']


    i=0
    #mapping: going through each detected pixel, assigning an alpha angles to it
    xoff=p['xoff_um']/1000
    yoff=p['yoff_um']/1000
    halfwidth_mm=p['halfwidth_mm']
    halfheight_mm=p['halfheight_mm']
    xstretch=p['xstretch']
    ystretch=p['ystretch']
    xs2=(xs-xoff)*xstretch/100  #finer coordinates of all JF pixels [mm]
    ys2=np.abs(ys-yoff)*ystretch/100
    ys2=(ys-yoff)*ystretch/100

    ysm,xsm=np.meshgrid(ys2,xs2)
    sel1=np.abs(xsm)<p['halfwidth_mm']
    sel2=np.abs(ysm)<p['halfheight_mm']
    sel=np.logical_and(sel1,sel2)

    if p['horizontal_crystal_offset']!=0:
        sel_hco=ysm<0
        xsm[sel_hco]=xsm[sel_hco]+p['horizontal_crystal_offset']

    aXs=interpAlX(xsm,ysm,grid=False)
    aYs=interpAlY(xsm,ysm*-1,grid=False)
    aYs_m=interpAlY(xsm,ysm,grid=False)
    aYs[aYs_m>aYs]=aYs_m[aYs_m>aYs]*-1
    aYs=aYs*-1
    #ys2a=np.array(np.dot(np.matrix(np.zeros(512)+1).transpose(),np.matrix(ys2)))
    # %%
    aXf=aXs[sel].flatten()
    aYf=aYs[sel].flatten()
#    aYf[ysf<0]=aYf[ysf<0]*-1
    data=im.transpose()[sel].flatten()
    aRf=(aXf**2 + aYf**2 )**0.5

    points=np.zeros((10,np.size(aXf)))
    points[0,:]=aXf
    points[1,:]=aYf
    points[2,:]=data
    points[3,:]=aRf
    rotation=p['rotation']
    if rotation!=0:
        points=rotate(points,rotation)

    return points



# %%##############################################################################
def draw_unwrapping(p,points,im,alRange,sigup,sigdown,sigupndF,sigdownndF,rawclimmax=20,radialclimmax=1,radialplotymax=20,radialplotymin=1):
    print('-- Draw unwrapping.')
    mradmax=p['draw_max_mrad']
    marksize=0.5

    ring_ns=np.arange(8)+1
    ring_qs=2*np.pi/p['draw_nanoshperes_size']*ring_ns
    lambd=12398/p['xfel_energy']/10 #nm
    qc=2*np.pi/lambd #conversion between divergence angle alpha=2theta[mrad] and q [nm-1]
    ring_alphas=ring_qs/qc
    rB=ring_alphas[0]

    if 1:
        fig= plt.figure(figsize=(17,10))

        plt.subplot(231)   #raw data
        plt.imshow(im)
        #plt.xlim(200,600)
        #plt.ylim(000,400)
        plt.title('raw data [px]')
        plt.text(20,20,p['name'],color='white')
        plt.colorbar()
        plt.clim(0,rawclimmax)

    # %
        plt.subplot(232)   #unwrapped data
        plt.scatter(points[0,:]*1e3,points[1,:]*1e3,c=np.log10(points[2,:]),s=marksize)
        #plt.xlabel('alpha X [mrad]')
        #plt.ylabel('alpha Y [mrad]')
        plt.title('unwraped, log-scale [mrad]')
        ax = plt.gca()
        r=rB*1e3*2
        lwc=0.5
        ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
        ax.add_patch(ellipse)
        r=2*rB*1e3*2
        ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
        ax.add_patch(ellipse)
        r=3*rB*1e3*2
        ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
        ax.add_patch(ellipse)
        plt.colorbar()
        plt.axis('equal')
        plt.xlim(-mradmax,mradmax)
        plt.ylim(-mradmax,mradmax)
        it='xoff {:.0f}\nyoff {:.0f} \nXstretch {:.1f}\nYstretch {:.1f}\nrotation {:.0f}°'.format(p['xoff_um'],p['yoff_um'],p['xstretch'],p['ystretch'],p['rotation'])
        it=it+"\nhor.cryst.off{:.1f}".format(p['horizontal_crystal_offset'])
        plt.text(-mradmax+2,mradmax-6,it,color='red')

    # %p

        plt.subplot(233) #Radial integrals
        points3=np.copy(points)
        points3[2,points[1,:]>0] = np.nan
        plt.plot(points3[3,:]*1e3,points3[2,:],'b.',markersize=0.5)
        plt.grid()

        points2=np.copy(points)
        points2[2,points[1,:]<0] = np.nan
        plt.plot(points2[3,:]*1e3,points2[2,:],'r.',markersize=0.5)
            #zoom
        plt.ylim(radialplotymin,radialplotymax)
        plt.xlim(0,mradmax)

        plt.semilogy(alRange*1e3,sigup,linewidth=3,color=[0,0,0.5],label='down')
        plt.plot(alRange*1e3,sigdown,linewidth=3,color=[0.5,0,0],label='up')

        plt.semilogy(alRange*1e3,sigupndF,'w',linewidth=1)
        plt.plot(alRange*1e3,sigdownndF,'w',linewidth=1)
        sig3rd=sigupndF+sigdownndF
        plt.plot(alRange*1e3,sig3rd,'k',linewidth=2)

        plt.vlines(ring_alphas*1e3,1e0,1e4,color=[0.3,0.5,0.3],label=str(p['draw_nanoshperes_size'])+' nm')
        plt.xlabel(r'$2\theta$ [mrad]')
        plt.legend()
        plt.title('Radial average')


    # %

        t4 = time.time()

        plt.subplot(234)   # spherical signal
        if 0:
            plt.title('radially averaged signal')
            cl1=-0.5
            cl2=radialclimmax
            selleft=points[0,:]<0
            plt.scatter(points[0,selleft]*1e3,points[1,selleft]*1e3,c=np.log10(points[6,selleft]),s=marksize)
            plt.clim(cl1,cl2)

            selleft=points[0,:]>0
            plt.scatter(points[0,selleft]*1e3,points[1,selleft]*1e3,c=np.log10(points[7,selleft]),s=marksize)

            plt.colorbar()
            plt.axis('equal')
            plt.xlim(-mradmax,mradmax)
            plt.ylim(-mradmax,mradmax)
            plt.clim(cl1,cl2)

        sel=points[9,:].astype('bool')
        on_crystal=sel
        plt.scatter(points[0,sel]*1e3,points[1,sel]*1e3,c=np.log10(points[2,sel]),s=marksize)
        plt.title('unwraped, log-scale, on-crystal [mrad]')
        plt.colorbar()
        plt.axis('equal')
        plt.xlim(-mradmax,mradmax)
        plt.ylim(-mradmax,mradmax)

        plt.subplot(235)   #flatfield
        plt.title('flatfield')

        plt.scatter(points[0,sel]*1e3,points[1,sel]*1e3,c=points[4,sel],s=marksize)
        plt.clim(0.5,2.0)
        plt.axis('equal')
        plt.xlim(-mradmax,mradmax)
        plt.ylim(-mradmax,mradmax)
        plt.colorbar()

        if 0:
            ax = plt.gca()
            rB=3.7
            #rB=0
            r=rB
            ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
            ax.add_patch(ellipse)
            r=2*rB
            ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
            ax.add_patch(ellipse)
            r=3*rB
            ellipse = Ellipse(xy=(0,0), width=r, height=r, edgecolor='w', fc='None', lw=lwc)
            ax.add_patch(ellipse)

        if 0:
            plt.subplot(236)   #Damage
            plt.title('damaged regions')
            plt.scatter(points[0,:]*1e3,points[1,:]*1e3,c=points[5,:],s=2)
            plt.colorbar()
            plt.axis('equal')
            plt.xlim(-mradmax,mradmax)
            plt.ylim(-mradmax,mradmax)
            plt.clim(0.5,1.0)

        plt.subplot(236)   #2nd flatfield
        plt.title('2nd flatfield')
        plt.scatter(points[0,:]*1e3,points[1,:]*1e3,c=points[8,:],s=marksize)
        plt.clim(0.7,1.5)
        plt.clim(0.5,2)
        plt.axis('equal')
        plt.xlim(-mradmax,mradmax)
        plt.ylim(-mradmax,mradmax)
        plt.colorbar()


        pars='_coff{:0.0f}_st{:04d}_{:04d}_xoff{:04d}_yoff{:04d}'.format(p['horizontal_crystal_offset']*100+1000,int(np.round(p['xstretch']*10)),int(np.round(p['ystretch']*10)),p['xoff_um']+1000,p['yoff_um']+1000)

        plt.savefig('unwrapped_'+p['name']+pars+' .png' , bbox_inches ='tight',dpi=140)


def draw_unwrapping_fast(p,points,im,alRange,sigup,sigdown,sigupndF,sigdownndF,rawclimmax=20,radialclimmax=1,radialplotymax=20,radialplotymin=1,second=1):
    mradmax=p['draw_max_mrad']
    marksize=3

    if 1:
        plt.figure(figsize=(13,10))

        it='xoff {:.0f}\nyoff {:.0f} \nXstretch {:.1f}\nYstretch {:.1f}\nrotation {:.0f}°'.format(p['xoff_um'],p['yoff_um'],p['xstretch'],p['ystretch'],p['rotation'])
        it=it+"\nhor.cryst.off{:.1f}".format(p['horizontal_crystal_offset'])
        plt.text(-mradmax+2,mradmax-6,it,color='red',fontsize=20)

        if not second:
            plt.title('flatfield')
    #       xi,yi,imi,ff,d=interpolate_scattering(points,x_max=12,x_step=0.1,y_max=12,y_step=0.1,do_flatfield=1)
    #      plt.pcolor(xi,yi,ff)
            plt.scatter(points[0,:]*1e3,points[1,:]*1e3,c=points[4,:],s=marksize)
            #plt.clim(2000,3000)#
            plt.clim(0.5,2.0)
        else:
            plt.title('2nd flatfield')
     #       xi,yi,imi,ff,d=interpolate_scattering(points,x_max=12,x_step=0.1,y_max=12,y_step=0.1,do_flatfield=1)
      #      plt.pcolor(xi,yi,ff)
            plt.scatter(points[0,:]*1e3,points[1,:]*1e3,c=points[8,:],s=marksize)
            #plt.clim(2000,3000)#
            plt.clim(0.5,2.0)

        plt.axis('equal')
        plt.xlim(-mradmax,mradmax)
        plt.ylim(-mradmax,mradmax)
        plt.colorbar()


        pars='_coff{:0.0f}_st{:04d}_{:04d}_xoff{:04d}_yoff{:04d}_rot{:04d}'.format(p['horizontal_crystal_offset']*100+1000,int(np.round(p['xstretch']*10)),int(np.round(p['ystretch']*10)),p['xoff_um']+1000,p['yoff_um']+1000,int(p['rotation']*10+1800))

        plt.savefig('unwrapped_fast_'+p['name']+pars+'.jpg' , bbox_inches ='tight',dpi=140)


# %%##############################################################################
def draw_flatfielded_rings(points,p,alRange,sig,sigFF):
    print('--Drawing flatfielded rings.')
    ms=1 #marker size
    maxmrad=11
    maxmradr=10.3
    maxmrady=16
    minmrady=1.0
    clmin=0.3e-2
    clmax=2e3
    x=points[0,:]
    y=points[1,:]
    nx=x*1e3
    ny=y*1e3
    f_upper=y>0
    f_lower=y<0

    if 1:
        fig= plt.figure(figsize=(6,5))
        if 1:
            gskw='wspace=0.3'
            plt.subplot(221)
            dataintensity=points[2,:]
            plt.scatter(nx,ny,c=points[2,:],s=ms,cmap=rofl.cmap(),norm=matplotlib.colors.LogNorm())

            plt.ylabel(r'2$\theta_Y$ [mrad]')
            #plt.axis('equal')
            plt.xlim(-maxmrad,maxmradr)
            plt.ylim(minmrady,maxmrady)
            plt.yticks(np.arange(5, 16, step=5))
            plt.xticks(np.arange(-10, 11, step=5))
            plt.title('a) Raw data')
            plt.colorbar()
            plt.clim(clmin,clmax)
# %   draw the flatfield
        if 1:
            plt.subplot(222)
            flatintensity = points[5,:]
            upmean=np.nanmean(flatintensity[f_upper])
            downmean=np.nanmean(flatintensity[f_lower])
            flatintensity[f_upper]=flatintensity[f_upper]/upmean
            flatintensity[f_lower]=flatintensity[f_lower]/downmean
            plt.scatter(nx,ny,c=flatintensity,s=ms,cmap=rofl.cmap_nw())
            plt.xlim(-maxmrad,maxmradr)
            plt.ylim(minmrady,maxmrady)
            plt.yticks(np.arange(5, 16, step=5))
            plt.xticks(np.arange(-10, 11, step=5))
            plt.colorbar()
            plt.title("b) Flat field ")
        if 1: #flatfielded image
            plt.subplot(223)
            cca= points[6,:]
            cca[cca<1e-2]=1e-2
            plt.scatter(nx,ny,c=cca,s=ms,cmap=rofl.cmap(),norm=matplotlib.colors.LogNorm())
            plt.xlim(-maxmrad,maxmradr)
            plt.ylim(minmrady,maxmrady)
            plt.colorbar()

            plt.xlabel(r'2$\theta_X$ [mrad]')
            plt.ylabel(r'2$\theta_Y$ [mrad]')
            plt.title("c) Flat fielded data")
            plt.clim(clmin,clmax)
            plt.yticks(np.arange(5, 16, step=5))
            plt.xticks(np.arange(-10, 11, step=5))
# %

        #fig = plt.figure(figsize=(6,4),dpi=100)
        plt.subplot(224)

        alphamin=1.3

        lambd=12398/p['xfel_energy']/10 #nm
        qc=2*np.pi/lambd #conversion between divergence angle alpha=2theta[mrad] and q [nm-1]
        q=qc*alRange

        qmin=alphamin/qc
        qmin=0.088
        sel=(q>qmin)

        mirror_q_correction=1.0 #found as optical fit to direct measurement.

        plt.plot(q[sel]*mirror_q_correction,sigFF[sel]/np.nanmax(sigFF[sel])*0.55,linewidth=3,color=rofl.g(),label='Mirror')
        direct=np.loadtxt('direct_SAXS.txt')
        qd=direct[:,0]*10
        sig=direct[:,1]
        sig[sig<1e-5]=np.nan
        plt.semilogy(qd,sig/np.nanmax(sig)*1e3,color=rofl.b(),linewidth=1,label='Direct')
        plt.legend()
        plt.xlim(0.08,0.75)
        plt.ylim(1.0e-4,0.4)
        plt.title('d) Radial integral')
#SAS fit
        fit=np.loadtxt('M6.txt')
        plt.plot(fit[:,0]*10,fit[:,1]*3.5e-4,'k',linewidth=1,label="Model")
        #plt.grid()
        plt.xlabel(r'$q$ [nm$^{-1}$]')
        #plt.ylabel('intensity [a.u.]')
        plt.legend()


        fig.tight_layout(pad=0.8)
        plt.savefig('rosahami_flatfielded_'+p['dataname']+'.png' , bbox_inches ='tight',dpi=350)        #shot 49: sample 3	nanoshperes 80nm, 146.5	11	74.68
    #shot Timepix9: sample 3	nanospheres 80 nm 146.5	11
def rotate(points,rotation_deg):
    rotation=rotation_deg/180*np.pi
    x=points[0,:]
    y=points[1,:]
    r=(x**2 + y**2)**0.5
    phi=np.arctan2(x,y)
    nphi=phi+rotation
    nx=r*np.sin(nphi)
    ny=r*np.cos(nphi)
    points[0,:]=nx
    points[1,:]=ny
    return points

def expand(rec,e):
    exp=np.copy(rec)
    exp[0]=exp[0]-e
    exp[1]=exp[1]+e
    exp[2]=exp[2]-e
    exp[3]=exp[3]+e
    return exp

def expandV(rec,e):
    exp=np.copy(rec)
    exp[2]=exp[2]-e
    exp[3]=exp[3]+e
    return exp

def getFlatfieldRect(rec,e):
    cx=(rec[0]+rec[1])/2
    cy=(rec[2]+rec[3])/2
    ff=np.array((cx-e,cx+e,cy-e,cy+e))
    return ff

def drawRect(a,lwb):
    plt.plot((a[0],a[0],a[1],a[1],a[0]),(a[2],a[3],a[3],a[2],a[2]),color='k',linewidth=lwb)
    a=expand(a,-0.007)
    plt.plot((a[0],a[0],a[1],a[1],a[0]),(a[2],a[3],a[3],a[2],a[2]),color='w',linewidth=lwb)


def calculate_peaks(p,areas,points,flatfield):
    numpeaks=np.shape(areas)[0]
    peaks=np.zeros((numpeaks,7))
    nx=points[0,:]*1e3
    ny=points[1,:]*1e3
    photon_energy = p['xfel_energy']*1e-3# 8.15keV
    for i in np.arange(numpeaks):
        a=areas[i,:]
        b=expand(a,p['expand_radius'])
        f=getFlatfieldRect(a,p['flatfield_radius'])

        selX=np.logical_and(nx>a[0],nx<a[1])
        selY=np.logical_and(ny>a[2],ny<a[3])
        sel=np.logical_and(selX,selY)

        selX=np.logical_and(nx>b[0],nx<b[1])
        selY=np.logical_and(ny>b[2],ny<b[3])
        selB=np.logical_and(selX,selY)
        selB=np.logical_xor(sel,selB) #surrounding area for background

        selX=np.logical_and(nx>f[0],nx<f[1])
        selY=np.logical_and(ny>f[2],ny<f[3])
        selF=np.logical_and(selX,selY)


        numpoints=np.sum(sel) #number of points in peak region
        numpointsflat=np.sum(selF) #number of points in peak region
        m1=np.nanmean(points[2,sel]) #keV/px in peak region
        m1b=np.nanmean(points[2,selB]) #average value of background, keV/px in bck region
        backdev=np.std(points[2,selB])# standrad deviation of background
        m1c=(m1-m1b)*numpoints #integrated intensity, backgound subtracted; [keV above background]
        m1c=m1c/photon_energy*p['data_numframes']  #[ph. in peak per all shots]
        m2=np.nanmean(flatfield[9,selF]) #mean of flatfield [keV/px]
        m2=m2/photon_energy *p['data_numframes']*numpointsflat  # photons in flatfield[ph, per all shots]
        m1ce=3*np.sqrt(m1c)  #3sigma uncertainity of m1c (poisson)
        m2e=3*np.sqrt(m2)
        #m1be=3*np.sqrt(m1b/photon_energy*numpoints*numframes) error of background
        #           0  1    2  3  4    5    6
        peaks[i,:]=(m1,m1b,m1c,m2,m1ce,m2e, backdev)
        #0
    peak_intensity=peaks[:,2]/peaks[:,3]
    #2/3   , errors are in dE(2)=4, dE(3)=5
    #I = X/Y, dI = |I| *( (dX/X)^2 + (dY/Y)^2     )*0.5
    #needto be checked::
    peak_intensity_error_rel= ((peaks[:,4]/peaks[:,2])**2 + (peaks[:,5]/peaks[:,3])**2 +( peaks[:,6]**2/peaks[:,2]) )**0.5
    peak_intensity_error=np.multiply(np.abs(peak_intensity),peak_intensity_error_rel)
    peaks[:,0]=peak_intensity
    peaks[:,1]=peak_intensity_error

    return peaks


def draw_grating_figs(points,flatfield,peaks,peak_indexes,areas,p,xlim=8,ylim=1):
    print('-- Drawing grating figs.')
    numpeaks=np.shape(areas)[0]
    cb=np.array((0.8,0.6,0.4))
    lwb=0.5
    nx=points[0,:]*1e3
    ny=points[1,:]*1e3
    ms=45 #marker size
    if 1:
        fig,(ax1,ax2) = plt.subplots(figsize=(16,4),nrows=2,sharex=True)
        plt.axes(ax1)

        plt.scatter(nx,ny,c=np.log10(points[2,:])+1.8,s=ms,cmap=rofl.cmap())
        plt.xlim(-xlim,xlim)
        plt.ylim(-ylim,ylim)
#        plt.plot([-10,10],[0,0],'w',linewidth=0.3)
        #plt.xlabel('alpha X [mrad]')
        #plt.ylabel('alpha Y [mrad]')
        plt.title('a) Scattering on grating (logarithmic colorscale)')
#        plt.text(-7.8,0.6,"photons in peak:",fontsize=10,color=cb*1.2)
        #plt.colorbar()
        plt.clim(0,5)

        for i in np.arange(numpeaks):
            a=areas[i,:]
            plt.plot((a[0],a[0],a[1],a[1],a[0]),(a[2],a[3],a[3],a[2],a[2]),color=cb,linewidth=lwb)

            b=expand(a,p['expand_radius'])
            plt.plot((b[0],b[0],b[1],b[1],b[0]),(b[2],b[3],b[3],b[2],b[2]),color=cb,linewidth=lwb)
            if ~np.isnan(peaks[i,2]):
                #plt.text(b[0],0.6,"{:2.0f}".format(peaks[i,2]),fontsize=10,color=cb*1.2)
                plt.text(b[0],0.6,"{:d}".format(peak_indexes[i]),fontsize=10,color=cb*1.2)

    # Draw the flatfield
        plt.axes(ax2)
        flatintensity = np.copy(flatfield[8,:])
     #   f_upper=ny>0
    #    f_lower=ny<0
   #     upmean=np.nanmean(flatintensity[f_upper])
  #      downmean=np.nanmean(flatintensity[f_lower])
 #       flatintensity[f_upper]=flatintensity[f_upper]/upmean
#        flatintensity[f_lower]=flatintensity[f_lower]/downmean
        ax2.scatter(nx[:],ny[:],c=flatintensity,s=ms,cmap=rofl.cmap())
        plt.xlim(-xlim,xlim)
        plt.ylim(-ylim,ylim)

#        plt.plot([-10,10],[0,0],'w',linewidth=0.3)
        plt.xlabel(r'scattering angle 2$\theta$ [mrad]')
        plt.title("b) Flat field (linear colorscale)")
        #plt.clim(0.5,2.)

        # peak markers & count
        cb=np.array((0.8,0.6,0.4))*1.2
        plt.text(-7.8,0.5,"photons in flatfield:",fontsize=10,color='r')

        for i in np.arange(numpeaks):
            a=getFlatfieldRect(areas[i,:],p['flatfield_radius'])
            drawRect(a,lwb)
            plt.text(a[0],0.25,"{:2.0f}".format(peaks[i,3]),fontsize=6,color='r')


        plt.savefig('rosahami_grating_figure_'+p['dataname']+'.png' , bbox_inches ='tight',dpi=200)

def draw_grating_peaks(peaks,peak_indexes,p,peaks_ref):
    peak_intensity=peaks[:,0]
    peak_intensity_error=peaks[:,1]

    plt.figure(figsize=(10,8))

    peaknumL=peak_indexes*1.0
    peaknumL[peaknumL>0]=np.nan
    peaknumL=peaknumL*-1
    peaknumR=peak_indexes*1.0
    peaknumR[peaknumR<0]=np.nan

    ms=7
    cs=6
    if np.size(peaks_ref)>0:
        peak_ri=peaks_ref[:,0]*4
        peak_rie=peaks_ref[:,1]*4
        plt.semilogy(peaknumR,peak_ri,'-',label='accumulation',markersize=ms,linewidth=2,color=rofl.g2())
        plt.errorbar(peaknumR,peak_ri,yerr=peak_rie,fmt='none',color=rofl.g3(),capsize=cs,capthick=2,elinewidth=2)


    a=plt.semilogy(peaknumL,peak_intensity,'o-',label='single shot left',markersize=ms,linewidth=2,color=rofl.o())
    b=plt.semilogy(peaknumR,peak_intensity,'*-',label='single shot right',markersize=ms,linewidth=2,color=rofl.b())
    plt.errorbar(peaknumL-0.03,peak_intensity,yerr=peak_intensity_error,fmt='none',color=a[0].get_color(),capsize=cs,capthick=2,elinewidth=2)
    plt.errorbar(peaknumR+0.03,peak_intensity,yerr=peak_intensity_error,fmt='none',color=b[0].get_color(),capsize=cs,capthick=2,elinewidth=2)

    manualminerror=np.exp(np.log(peak_intensity)-np.log(peak_intensity-peak_intensity_error))
    manualmaxerror=np.exp(np.log(peak_intensity+peak_intensity_error)-np.log(peak_intensity))

    plt.errorbar(peaknumR+0.03,peak_intensity,yerr=manualminerror,fmt='none',color='b',capsize=cs,capthick=2,elinewidth=1)
    plt.errorbar(peaknumR+0.03,peak_intensity,yerr=manualmaxerror,fmt='none',color='r',capsize=cs,capthick=2,elinewidth=1)



    plt.legend()
#    plt.xlim(2.3,7.5)
    plt.ylim(1e-1,1e5)
    plt.grid()
    plt.xticks(np.abs(peak_indexes))
    plt.xlabel('peak number')
    plt.ylabel('intensity [a.u.] ')
    plt.title('run #100, train #567')
    plt.savefig('rosahami_grating_peaks_'+p['dataname']+'.png' , bbox_inches ='tight',dpi=300)


def generate_defs(peak_indexes,spacing,hor_size,vert_size,y_offset,x_off=0):
    numpeaks=np.size(peak_indexes)
    defs=np.zeros((numpeaks,4))
    defs[:,0]=peak_indexes*spacing
    defs[:,0]=defs[:,0]+x_off
#    defs[defs[:,0]>0,0]=defs[defs[:,0]>0,0]+x_off
 #   defs[defs[:,0]<0,0]=defs[defs[:,0]<0,0]-x_off
    defs[:,1]=y_offset
    defs[:,2]=hor_size
    defs[:,3]=vert_size
    return defs


def defs_to_areas(defs):
    areas=np.copy(defs)
    areas[:,0]=defs[:,0]-defs[:,2]
    areas[:,1]=defs[:,0]+defs[:,2]
    areas[:,2]=defs[:,1]-defs[:,3]
    areas[:,3]=defs[:,1]+defs[:,3]
    return areas


def do_flatfield(points,p,separated=0):
    #Removing the gap:
    points[2,np.abs(points[1,:])<p['gap_halfwidth']] = np.nan

    # Getting the radial averages - Sigup and Sigdown
    da=p['alpha_step']
    alRange=np.arange(0,p['alpha_max'],da)
    sel_crystal=points[2,:]>p['lower_threshold']

    sigup = do_radial_average(alRange,points,(points[1,:]<0)*sel_crystal)
    sigdown = do_radial_average(alRange,points,(points[1,:]>0)*sel_crystal)

    # Creating the radially averaged map
    ram = make_radial_scattering(alRange,sigdown,sigup,points)
    points[6,:]=ram #radial average, separately calculated for top & bottom
    points[4,:]=points[2,:]/ram #flat field

    # The damage map
    dam1=points[4,:]<p['damage_threshold']
    dam2=points[4,:]>p['halo_threshold']
    points[5,:]=np.logical_or(dam1,dam2)#damage
    points[9,:]=-1*sel_crystal


    # 2nd signal: taking into account damage map
    selnondamaged=np.logical_not(points[5,:])
    selnondamaged=np.logical_and(selnondamaged,points[9,:])

    sigupnd   = do_radial_average(alRange,points,np.logical_and(points[1,:]<0,selnondamaged))
    sigdownnd = do_radial_average(alRange,points,np.logical_and(points[1,:]>0,selnondamaged))

    # Smoothing
    sigupndF=sigupnd
    sigdownndF=sigdownnd
    try:
        sigupnd2=sigupnd[np.isfinite(sigupnd)]
        sigdownnd2=sigdownnd[np.isfinite(sigdownnd)]
        sigdownnd2=scipy.signal.savgol_filter(sigdownnd2, p['radial_filter_strength'], 2)
        sigupnd2=scipy.signal.savgol_filter(sigupnd2, p['radial_filter_strength'], 2)
        sigupndF[np.isfinite(sigupnd)]=sigupnd2
        sigdownndF[np.isfinite(sigdownnd)]=sigdownnd2
    except:
        print('Savgoy filter failed')
        sigupndF=sigupnd
        sigdownndF=sigdownnd


    # Creating the second radially averaged map
    ram = make_radial_scattering(alRange,sigdownndF,sigupndF,points)
    points[7,:]=ram
    points[8,:]=points[2,:]/ram
    # Removing the damaged things
    #points[8,points[5,:].astype(bool)]=np.nan
    #removign the on-crystal thing
    points[8,np.logical_not(points[9,:].astype(bool))]=np.nan

    if separated:
        #3rd: doing the flat field together for both up & down crystals
        ram = make_radial_scattering(alRange,sigdownndF,sigupndF,points)
    else:
        #3rd: doing the flat field together for both up & down crystals
        sig3rd=(sigdownndF+sigupndF)/2
        ram = make_radial_scattering(alRange,sig3rd,points=points)
#    points[9,:]=points[2,:]/ram
    # Removing the damaged things
 #   points[9,points[5,:].astype(bool)]=np.nan

    # Saving all into a file
    fn=p['name'].replace('.tif','')
    pickle.dump((points,p),open( fn+'_flatfield.pickle', "wb" ))

    #4 flatfield
    #5 damage boolean map
    #6 radialy smoothed signal
    #7 2nd radialy smoothed signal - (taking into account damage)
    #8 2nd flatfiled - (taking into account damage, and it is radialy slightly smoothed)
    #9 oncrystal boolean map
    return points,alRange,sigup,sigdown,sigupndF,sigdownndF

def interpolate_scattering(points,x_max=12,x_step=0.1,y_max=12,y_step=0.1,do_flatfield=1):
    nx=points[0,:]*1e3 #mrad
    ny=points[1,:]*1e3

    xi = np.arange(-x_max,x_max,x_step)
    yi = np.arange(-y_max,y_max,y_step)
    xi,yi = np.meshgrid(xi,yi)

    data = griddata((nx,ny),points[2,:],(xi,yi),method='linear')
    if do_flatfield:
        ff = griddata((nx,ny),points[5,:],(xi,yi),method='linear')
        flatfielded = data/ff
        return xi,yi,data,ff,flatfielded
    else:
        return xi,yi,data,data*0,data*0

def interpolate_scattering_q(points,x_max=12,x_step=0.1,y_max=12,y_step=0.1,do_flatfield=1,XFEL_photon_energy=8150):
    nx=points[0,:]#rad
    ny=points[1,:]

    lambd=12398/XFEL_photon_energy/10 #nm
    qc=2*np.pi/lambd #conversion between divergence angle alpha=2theta[mrad] and q [nm-1]
    qx=qc*nx
    qy=qc*ny

    xi = np.arange(-x_max,x_max,x_step)
    yi = np.arange(-y_max,y_max,y_step)
    xi,yi = np.meshgrid(xi,yi)

    data = griddata((qx,qy),points[2,:],(xi,yi),method='linear')
    if do_flatfield:
        ff = griddata((qx,qy),points[5,:],(xi,yi),method='linear')
        flatfielded = data/ff
        return xi,yi,data,ff,flatfielded
    else:
        return xi,yi,data,data*0,data*0


def radial_average_q(points,r_max=12,r_step=0.1,XFEL_photon_energy=8150):
#    nx=points[0,:]#rad
 #   ny=points[1,:]

    lambd=12398/XFEL_photon_energy/10 #nm
    qc=2*np.pi/lambd #conversion between divergence angle alpha=2theta[mrad] and q [nm-1]
 #   qx=qc*nx
  #  qy=qc*ny

#    xi = np.arange(-x_max,x_max,x_step)
 #   yi = np.arange(-y_max,y_max,y_step)
  #  xi,yi = np.meshgrid(xi,yi)

    ri = np.arange(0,r_max,r_step)
    alRange=ri/qc
    sel=points[0,:]*0+1
    data=do_radial_average(alRange,points,sel,column = 2)
    ff=do_radial_average(alRange,points,sel,column = 5)

#    data = griddata((qx,qy),points[2,:],(xi,yi),method='linear')
#    ff = griddata((qx,qy),points[5,:],(xi,yi),method='linear')
    flatfielded = data/ff
#        return xi,yi,data,ff,flatfielded
 #   else:
  #      return xi,yi,data,data*0,data*0
    
    return ri,data,ff,flatfielded

def tick(lab=''):
    global times, time_labels
    import time
    times.append(time.time())
    time_labels.append(lab)

def print_times():
    tick('end')
    global times, time_labels
    for i,t in enumerate (np.diff(times)):
        lab=time_labels[i]
        if lab!='':
            print("{:.0f}: {:.1f}s (".format(i+1,t)+lab+')')
        else:
            print("{:.0f}: {:.1f}s".format(i+1,t))

def clear_times():
    global times, time_labels
    times=[]
    time_labels=[]
