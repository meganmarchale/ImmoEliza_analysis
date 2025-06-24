import pandas as pd




def main():
    filename = "./data/immoweb-dataset.csv"
    df = pd.read_csv(filename)
    # function 

  
 
    
    
    # save to new cleaned file
    df.to_csv("./data/cleaned_data.csv", index=True)

if __name__ == "__main__":
    main()



