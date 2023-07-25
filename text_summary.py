import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """The Asgardian Loki encounters the Other, the leader of an extraterrestrial race known as the Chitauri. In exchange for retrieving the Tesseract,[c] a powerful energy source of unknown potential, the Other promises Loki an army with which he can subjugate Earth. Nick Fury, director of the espionage agency S.H.I.E.L.D., arrives at a remote research facility, where physicist Dr. Erik Selvig is leading a team experimenting on the Tesseract. The Tesseract suddenly activates and opens a wormhole, allowing Loki to reach Earth. Loki steals the Tesseract and uses his scepter to enslave Selvig and other agents, including Clint Barton, to aid him.

In response, Fury reactivates the "Avengers Initiative". Agent Natasha Romanoff heads to Kolkata to recruit Dr. Bruce Banner to trace the Tesseract through its gamma radiation emissions. Fury approaches Steve Rogers to retrieve the Tesseract, and Agent Phil Coulson visits Tony Stark to have him check Selvig's research. Loki is in Stuttgart, where Barton steals the iridium needed to stabilize the Tesseract's power, leading to a confrontation with Rogers, Stark, and Romanoff that ends with Loki's surrender. While Loki gets escorted to S.H.I.E.L.D., his adoptive brother Thor arrives and frees him, hoping to convince him to abandon his plan and return to Asgard. Stark and Rogers intervene and Loki is taken to S.H.I.E.L.D.'s flying aircraft carrier, the Helicarrier, where he is imprisoned.

The Avengers become divided over how to approach Loki and the revelation that S.H.I.E.L.D. plans to harness the Tesseract to develop powerful weapons as a deterrent against hostile extraterrestrials. As they argue, Loki's agents attack the Helicarrier, and the stress causes Banner to transform into the Hulk. Stark and Rogers work to restart the damaged engine, and Thor attempts to stop the Hulk's rampage. Romanoff knocks Barton unconscious, breaking Loki's mind control. Loki escapes after killing Coulson and Fury uses Coulson's death to motivate the Avengers into working as a team. Loki uses the Tesseract and a wormhole generator Selvig built to open a wormhole above Stark Tower to the Chitauri fleet in space, launching his invasion.

Rogers, Stark, Romanoff, Barton, Thor, and the Hulk rally in defense of New York City, and together the Avengers battle the Chitauri. The Hulk beats Loki into submission. Romanoff makes her way to the generator, where Selvig, freed from Loki's mind control, reveals that Loki's scepter can shut down the generator. Fury's superiors from the World Security Council attempt to end the invasion by launching a nuclear missile at Midtown Manhattan. Stark intercepts the missile and takes it through the wormhole toward the Chitauri fleet. The missile detonates, destroying the Chitauri mothership and disabling their forces on Earth. Stark's suit loses power and he goes into freefall, but the Hulk saves him, while Romanoff uses Loki's scepter to close the wormhole. In the aftermath, Thor returns with Loki and the Tesseract to Asgard, where Loki will face their justice.

In a mid-credits scene, the Other confers with his master[d] about the failed attack on Earth."""

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')  
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text]+=1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)


    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    # print(sent_scores)

    select_len = int (len(sent_tokens)*0.3)
    # print(select_len)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print("length of original text ", len(text.split(' ')))
    # print("length of summary text ",len(summary.split(' ')) )

    return summary, doc , len(rawdocs.split(' ')) , len(summary.split(' '))