import torch
import difflib
import whisper


def recognize_audio(filename):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = whisper.load_model("base", device=device)
    if device == "cuda":
        print("using cuda", device)
        model = model.half()
    result = model.transcribe(filename)
    return result


from Levenshtein import distance as lev_distance

def compare_texts(reference, hypothesis):
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    
    diff = difflib.SequenceMatcher(None, ref_words, hyp_words)
    
    result = []
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag == 'replace':
            for ref_word, hyp_word in zip(ref_words[i1:i2], hyp_words[j1:j2]):
                if lev_distance(ref_word, hyp_word) <= len(ref_word) // 2:  
                    result.append(f"[{ref_word} -> {hyp_word}]")
                else:
                    result.append(f"[{ref_word} -> ]")
                    result.append(f"[ -> {hyp_word}]")
        elif tag == 'delete':
            for ref_word in ref_words[i1:i2]:
                result.append(f"[{ref_word} -> ]")
        elif tag == 'insert':
            for hyp_word in hyp_words[j1:j2]:
                result.append(f"[ -> {hyp_word}]")
        else:  # equal
            result.extend(ref_words[i1:i2])
    
    return ' '.join(result)
