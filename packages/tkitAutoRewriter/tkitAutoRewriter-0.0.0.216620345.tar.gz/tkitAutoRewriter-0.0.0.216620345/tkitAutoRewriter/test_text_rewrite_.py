from tkitAutoRewriter import AutoReWrite, SentenceClassification
from tkitAutoRewriter.diff import similar_diff_qk_ratio
from tkitAutoRewriter.api import get_markdown_images_format
import re
text = """

hello Border Collie
Prized for his intelligence, herding instinct and working ability, the Border Collie was developed more than a century ago in Britain.![这是图片](/assets/img/philly-magic-garden.jpg "Magic Gardens")  An intense and tractable worker, the Border Collie is a highly energetic breed that thrives with vigorous exercise, a job and space to run.

The Border Collie is an affectionate family dog that does best with mature children due to his tendency to herd people. His coat sheds seasonally and requires regular brushing.

DID YOU KNOW? The Border Collie became popular in the 19th century when Queen Victoria became a fan of the breed.

ALSO KNOWN AS: Scottish Sheep Dog; sometimes confused with the related Welsh Sheep Dog ('ci defaid' in Welsh)






![grey and white spotted dog laying down under a blanket](https://i.shgcdn.com/8cd735ff-430c-4d47-a027-961ce32d0c77/-/format/auto/-/preview/3000x3000/-/quality/lighter/)

* * *

Seizures can be scary events to witness, especially if it’s your first time seeing one, and especially if it’s happening to your furry best friends. What are some things to keep in mind, and how can you help your pup if he is having one?

* * *

##  What causes seizures in dogs?

There are many different causes of seizures in dogs. Idiopathic epilepsy is the most common cause. Epilepsy is an inherited condition where your dog will start to have seizures due to an unknown cause, which is the definition ofidiopathic. On average, epilepsy can develop in dogs between the ages of one and six years. Beagles, Labradors, German Shepherds, Collies, and Australian Shepherds are some of the most common breeds affected by idiopathic epilepsy.
Exposure to certain toxins can cause seizures in dogs. Illicit drugs and even pain medications like ibuprofen have been known to cause seizures. Foods that contain xylitol (a sugar substitute) and dark chocolate which has high concentrations of theobromine will cause sharp drops in your dog’s blood sugar, thus resulting in seizures if left untreated. Even mushrooms and certain plants like the seeds of a Sago’s palm can cause seizures when ingested.
Brain trauma or damage can result in seizures, and if your dog has a brain tumor, increased pressure inside of his skull due to inflammation can cause seizures. Other cancers elsewhere in the body can result in seizures if cancer has spread to the brain. Underlying organ disorders such as liver and kidney disease cause the buildup of toxins in the bloodstream, thus increasing the risk for seizure activity.
If your dog is prone to seizures, any change in brain activity can initiate a seizure. This means a seizure can be triggered when he is excited, anxious, scared, or even eating his food. Any medications or supplements that are known to lower seizure thresholds should be avoided.

* * *


"""
# # out=re.findall(r'!\\[[^\\]]+\\]\\([^\\)]+\\)', text)
# out=re.findall(r'(?:!\[(.*?)\]\((.*?)\))', text)  # 提最述与rul
# print(out)


# out=re.findall(r'(?:!\[(.*?)\))', text)  # 提最述与rul

# print("!["+out[0]+")")


# text=text.replace("!["+out[0]+")","\n\n!["+out[0]+")\n\n")


# text=get_markdown_images_format(text)

print(text)

# exit()







print("字数",len(text.split(" ")))

rewriter = AutoReWrite(api='http://192.168.1.18:3008',api_sbert_host="http://192.168.1.18:3016")


for temperature in [1.0,1.2,1.4,1.6,1.8,2.0]:
    out = rewriter.rewriter(text, simlimit=0.6, simlimitmax=0.999999999, auto_sample=False,temperature=temperature)

    print("temperature",temperature)
    # print(text)
    print("".join(out['items']))
    ratio = similar_diff_qk_ratio(text, "".join(out['items']))
    print(ratio)
    print("字数",len(" ".join(out['items']).split(" ")))