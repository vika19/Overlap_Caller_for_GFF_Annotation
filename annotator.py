import sys

bedops_in = sys.argv[1]
gff_in = sys.argv[2]
annot_out = sys.argv[3]

chrID=[]	#chromosome ID	
chrS=[]		#composite range start
chrE=[]		#composite range end
chrD=[]		#composite range direction*
match=[]	#match list for each range entry (list of lists - pos dir only)
matchneg=[]	#match list for each range entry (list of lists - neg dir only)
list=[]		#list of matches stored in match list

##parse ranges
range_file = open(bedops_in, "r")

for entry in range_file:
    entry=entry[:-1]
    line = entry.split("\t")
    chrID.append(line[0])
    chrS.append(int(line[1]))
    chrE.append(int(line[2]))
    match.append([])
    matchneg.append([])
    chrD.append("")

range_file.close()

#find which range gff entries belong in
gff = open(gff_in, "r")
j=0
for entry in gff:
    line = entry.split()
    ID = line[0]
    S = int(line[3])
    E = int(line[4])
    T = line[8]
    D = line[6]
    contlen = abs(S-E)
#    print j
    j=j+1
    print str(j) + " transcripts found"	#nice to have a progress marker!

    #run through start points to find where entry starts

    i=0 #start at line 1
    #for 0-last range entry
    for i in range(0,len(chrID)-1):
	print i
	if ID==chrID[i]:
            if S in range(chrS[i], chrS[i+1]):
	        if D=="+":
#		    print "POS"
		    list = match[i]
		    list.append(T + "(" + ID + " " + str(S) + ", " + str(E) + ", " + str(contlen) + ", " + D + ")" + "\t") 
	            match[i] = list  #update match list at line
#		    print match[i]
		    break
		elif D=="-":
#		    print "NEG"
		    list = matchneg[i]
		    list.append(T + "(" + ID + " " + str(S) + ", " + str(E) + ", " + str(contlen) + ", " + D + ")" + "\t") 
	            matchneg[i] = list  #update match list at line
#   		    print matchneg[i]
 	    	    break
##CLOSE FILE
gff.close()

##print ranges and matches
output = open(annot_out, "w")
for i in range(0,len(chrID)-1):
    if len(match[i]) > 0:
        line_out = chrID[i] + "\t" + str(chrS[i]) + "\t" + str(chrE[i]) + "\t" + ''.join(match[i]) + "\n"
        output.write(line_out)
    if len(matchneg[i]) > 0:
        line_out_neg = chrID[i] + "\t" + str(chrS[i]) + "\t" + str(chrE[i]) + "\t" + ''.join(matchneg[i]) + "\n"
        output.write(line_out_neg)


output.close()
