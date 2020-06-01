# Build intent classifier training data
import os
import csv

os.chdir("./Raw Data")
f = open("combined_diseases.txt", "r")
out = csv.writer(open('train.csv', 'w', newline=""))

out.writerow(["Text","Intent"])

for line in f:
    line = line.strip().lower()

    # short description
    out.writerow([line+" description","ShortDescription"])
    out.writerow([line+" descriptions","ShortDescription"])
    out.writerow(["describe "+line,"ShortDescription"])
    out.writerow(["explain "+line,"ShortDescription"])
    out.writerow(["can you explain "+line,"ShortDescription"])
    out.writerow(["can you explain "+line+"?","ShortDescription"])
    out.writerow(["can you describe "+line,"ShortDescription"])
    out.writerow(["can you describe "+line+"?","ShortDescription"])    
    out.writerow(["what is "+line,"ShortDescription"])
    out.writerow(["what is "+line+"?","ShortDescription"])
    out.writerow(["whats "+line,"ShortDescription"])
    out.writerow(["tell me about "+line,"ShortDescription"])
    out.writerow([line + " definition","ShortDescription"])
    out.writerow(["definition of "+ line,"ShortDescription"])
    out.writerow([line + " meaning","ShortDescription"])
    out.writerow([line,"ShortDescription"])

    # long description
    out.writerow([line+" long description","LongDescription"])
    out.writerow([line+" in-depth description","LongDescription"])
    out.writerow([line+" in depth description","LongDescription"])
    out.writerow([line+" details","LongDescription"])
    out.writerow(["detailed description of "+line,"LongDescription"])
    out.writerow(["give me a detailed description of "+line,"LongDescription"])
    out.writerow(["tell me a detailed description of "+line,"LongDescription"])

    # symptom
    out.writerow([line+" symptom","Symptom"])
    out.writerow([line+" symptoms","Symptom"])
    out.writerow([line+" signs","Symptom"])
    out.writerow([line+" sign","Symptom"])
    out.writerow([line+" indications","Symptom"])
    out.writerow([line+" indication","Symptom"])
    out.writerow([line+" syndrome","Symptom"])
    out.writerow([line+" syndromes","Symptom"])
    out.writerow([line+" evidence","Symptom"])
    out.writerow([line+" manifestation","Symptom"])
    out.writerow([line+" warning sign","Symptom"])
    out.writerow([line+" warning signs","Symptom"])
    out.writerow([line+" early warning signs","Symptom"])
    out.writerow(["warning signs of "+line,"Symptom"])
    out.writerow(["early signs of "+line,"Symptom"])
    out.writerow(["symptoms of "+line,"Symptom"])
    out.writerow(["how do i know if i have "+line+"?","Symptom"])
    out.writerow(["do i have "+line+"?","Symptom"])
    out.writerow(["do i have "+line,"Symptom"])

    # cause
    out.writerow([line+" cause","Cause"])
    out.writerow([line+" causes","Cause"])
    out.writerow([line+" reason","Cause"])
    out.writerow([line+" reason why","Cause"])
    out.writerow(["reason why "+line+" occurs?","Cause"])
    out.writerow(["why does "+line+" happen?","Cause"])
    out.writerow(["reasons behind "+line+"?","Cause"])
    out.writerow(["reason behind "+line+"?","Cause"])
    out.writerow(["what causes "+line,"Cause"])
    out.writerow(["what causes "+line+"?","Cause"])
    out.writerow(["can you tell me the causes of "+line,"Cause"])

    # treatment
    out.writerow([line+" treatments?","Treatment"])
    out.writerow([line+" treatment?","Treatment"])
    out.writerow([line+" treatment","Treatment"])
    out.writerow([line+" treatments","Treatment"])
    out.writerow([line+" cure","Treatment"])
    out.writerow(["how to cure "+line,"Treatment"])
    out.writerow([line+" medication","Treatment"])
    out.writerow([line+" medicine","Treatment"])
    out.writerow(["treatment for "+line,"Treatment"])
    out.writerow(["how do i treat "+line,"Treatment"])
    out.writerow(["medicine for "+line,"Treatment"])
    out.writerow(["what's medicine for "+line,"Treatment"])
    out.writerow(["what is medicine for "+line,"Treatment"])
    out.writerow(["medication for "+line,"Treatment"])
    out.writerow(["therapy for "+line,"Treatment"])
    out.writerow([line+" therapy","Treatment"])
    out.writerow([line+" healing","Treatment"])
    out.writerow([line+" remedy","Treatment"])
    out.writerow(["how to remedy "+line,"Treatment"])

    #infectiousness
    out.writerow(["how is " +line+" spread","Infectiousness"])
    out.writerow(["how is " +line+" spread?","Infectiousness"])
    out.writerow(["how is " +line+" transmitted?","Infectiousness"])
    out.writerow(["how contagious is " +line,"Infectiousness"])
    out.writerow(["how infectious is " +line,"Infectiousness"])
    out.writerow(["how did i get " +line+"?","Infectiousness"])
    out.writerow(["how do people get " +line,"Infectiousness"])
    out.writerow(["how do you get " +line+"?","Infectiousness"])

f.close()