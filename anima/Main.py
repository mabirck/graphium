
from Anima import Anima
if __name__ == '__main__':
    
    anima = Anima()
    anima.start()
    anima.generate_csvs()
    #preds = (np.argsort(probabilities_by_image)[::-1])[0:5]
    #for p in preds:
    #    print class_names[p], prob[p]
