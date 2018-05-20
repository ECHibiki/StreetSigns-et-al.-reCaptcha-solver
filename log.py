print("The following is documentation relating to the data gathering process.")
print("Data gathered by individuals on the datasets.verniy.xyz homepage.")
print("Ideal target 92.7%.")
print("\n\t--\t1st Attempt: May 13th, 2018\t--\n")
print("""
Best greyscale probability: 43.8462%
Best color probability: 62.0915%
""")
print(
"""Data gathering was done in stages depending on the quantities of data.
The first itteration made use of 1371 images(80%Train, 10%Valid, 10%Test)
distributed in the ratio of captcha images:
	roughly at the time 
	18% cars,
	16.5% buses,
	9.88% traffic lights,
	6.14% bridges,
	5.7% bicycles,
	5.4% crosswalks,
	4.76% mountains,
	3.43% taxis,
	2.53% boats,
	2.41% statues,
	2.49% firehydrants,
	1.45% motorcycles,
	0.904% roads,
excluding the percentages of full selection images, storefronts and palm.
Palm trees did not have enough data at this time and alternate sized
images such as street signs or storefronts are not yet added.
For the first itteration of developement in order to speed up work;
the train, validation and test data were shuffled by a php script on download
into it's relevant folders. Values are mostly hardcoded, but will probability
change as more optimization is done.""")
print()
print(
"""
Model is based on the TensorFlow MNIST CNN tutorial and
MicrocontrollersAndMore's tutorial based on it with edits wherever appropriate
'TensorFlow_Tut_1_Installation_and_First_Progs' found on github under his name.
Data processing and evaluatio is self-motivated
""")
print("Run initially on Windows7 with 8GB RAM")
print("\n\t--\t2nd Version: May 14th, 2018\t--\n")
print("""
Best greyscale probability: 57.5163%
Best color probability: 66.0915%
""")
print(
"""
Dataset ratios:
	18.6% cars,
	17% buses,
	9.39% traffic lights,
	5.84% bridges,
	5.58% crosswalks,
	5.38% bicycles,
	5.08% mountains,
	2.89% taxis,
	2.54% firehydrants,
	2.49% statues,
	2.44% boats,
	1.52% motorcycles,
	0.836% roads,
To get a quick working version a reduced set was used taking into account the highest probability of captchas found. 
Dataset size was also increased using . 
	Car groupings: Taxis, Cars and along with any other category that frequently has cars
	Mountains and Hills: Land masses are easy to recognize
	Firehydrants: Distinctly colored and unconfusable
	Statues: Unique shape
	Errors: Any unmentioned set is considered in a mass category of false data
Experiment Distribution against reality:
	Tested: 28.71%
	Ignoring: 71.29%
""")
print("\n\t--\t3rd Version: May 15th, 2018\t--\n")
print("""
Best color probability: 70.5%
""")
print(
"""
Same as before, but only cars or errors. Improved the distribution

iterations = 4000
loss_steps = 1e-4
batch_size = 50
base_complementary_dropout = 0.5 #lower means more dropout
channels = 3
classes = 2
#5 or 13
dimension_x = 100
dimension_y = 100
""")
print("\n\t--\t3rd Version: May 16th, 2018\t--\n")
print("""
Batch: 50
Best grey probability: 80.4348%
Best color probability: 81.5127%
Best color with grey probability: %
Batch: 25
Best grey probability: 80.4348%
Best color probability: 81.5127%
Best color with grey probability: 83.1522%
Batch: 3 
Iterations: 16000
Best color with grey probability: 82.6087%
~1500 train 
~184 test & valid
""")
print(
"""
Same as before, but only bus or errors.
Using an additional deep layer the best achievable model was `save1526467707.mod` at 83.1522% using 
Abandoning the test set due to lack of use(348bus vs 1348error): 83.6957%
""")
print("\n\t--\t4th Version: May 17th, 2018\t--\n")
print("""Canny Edge Detection was added: 79.34%
Canny Edge Detection was added as a 5th channel: %82.6
iterations = 1000
loss_steps = 1e-4
batch_size = 50
base_complementary_dropout = 0.5 #lower means more dropout

5channel: %83.6957

iterations = 16000
loss_steps = 1e-4
batch_size = 8
base_complementary_dropout = 0.5 #lower means more dropout
channels = 5
classes = 2

5channel with 90% vs 10% [437bus vs 1833 error] ===
iterations = 8000
loss_steps = 1e-4
batch_size = 8
base_complementary_dropout = 0.5 #lower means more dropout
channels = 5
classes = 2
""")
print("\n\t--\t4th Version: May 19th, 2018\t--\n")
print("""
Client side solver application and localhost server using flask
Might be more buggy than anticipated.
Used the 13 classes: 19.8962 against 40% validation

In practice, effects are starting to be seen http://puu.sh/AoYg1/a628b02025.jpg
Seems to struggle with objects in the distance on roads. Might consider a deeper pooling method
""")
input()
