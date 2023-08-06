def surveyaudios():
    import pandas as pd
    import os
    import shutil
    import pathlib

    print("¿Cuántas preguntas van a descargarse?")
    npreguntas=[]
    np0=int(input())
    for x in range(np0):
        print("QuestionIdx N° {}:".format(x+1))
        npreguntas.append(int(input()))

    n=[]
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        for x in filenames:
            n.append(str(x))

    n1=pd.DataFrame(n)
    n2=pd.DataFrame(n1.loc[n1[0].apply(lambda x: str(x).endswith(".xlsx"))==True][0]).reset_index(drop=True)
    alist=n2.loc[n2[0].apply(lambda x: str(x).endswith("alist.xlsx"))==True].iloc[0,0]
    noalist=n2.loc[n2[0].apply(lambda x: str(x).endswith("alist.xlsx"))==False].iloc[0,0]

    ejemplo_dir = os.getcwd()
    directorio = pathlib.Path(ejemplo_dir)
    ficheros = [fichero.name for fichero in directorio.iterdir() if fichero.is_file()]
    ficheros

    ficheros2=[]
    for x in os.listdir(os.getcwd()):
        ficheros2.append(x)

    ficheros3=list(set(ficheros).symmetric_difference(set(ficheros2)))

    for x in ficheros3:
        if os.path.isfile("{}/{}".format(x,alist)):
            carpeta=x

    prueba1=pd.read_excel("{}/{}".format(carpeta,alist)).copy()
    prueba3=prueba1.loc[prueba1["QuestionIdx"].apply(lambda x: x in npreguntas)==True].reset_index(drop=True)
    prueba2=pd.read_excel("{}/{}".format(carpeta,noalist)).copy()
    prueba2["grab"]=prueba2["SbjNum"].apply(lambda x: x in list(prueba3["SubjectID"]))
    prueba4=prueba2[["SbjNum","Srvyr","grab"]].rename(columns={"SbjNum":"SubjectID"})
    prueba5=prueba3.merge(prueba4, on="SubjectID")

    def contarpunto(i):
        b1=0
        b2=""
        for x in i:
            if x!=".":
                b2+=x
            else:
                break
        return "{}".format(b2.replace("\n","-"))

    preguntas=[]
    for x in list(prueba5["QuestionText"].value_counts().index):
        preguntas.append(str(x))

    pX=[]
    for x in npreguntas:
        pX.append(prueba5.loc[prueba5["QuestionIdx"]==x].reset_index(drop=True))


    ncarpeta="__datos__"

    try:
        shutil.rmtree(ncarpeta)
    except OSError as e:
        pass

    os.mkdir(ncarpeta) 


    for x in npreguntas:
        os.mkdir("{}/Q{}".format(ncarpeta,x))

    pr=0
    for i in pX:
        for x in i["Srvyr"].value_counts().index:
            os.mkdir(("{}/Q{}/{}").format(ncarpeta,npreguntas[pr],x))
        pr+=1


    list_errores=[]

    for i in range(len(pX)):
        for x in range(pX[i].shape[0]):
            try:
                shutil.copy("{}/{}_{}".format(carpeta,pX[i]["SubjectID"][x],pX[i]["Name"][x]),"{}/Q{}/{}/{}".format(ncarpeta,npreguntas[i],pX[i]["Srvyr"][x],pX[i]["Name"][x]))
            except:
                list_errores.append(pX[i]["Name"][x])

    prueba5.loc[prueba5["Name"].apply(lambda x: x in list_errores)==True].to_excel("{}/errores.xlsx".format(ncarpeta))
    print("Ya esta!")