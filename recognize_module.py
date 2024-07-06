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


def compare_texts(reference, hypothesis):
    diff = difflib.ndiff(reference.split(), hypothesis.split())

    result = []
    added_words = []
    removed_words = []

    for word in diff:
        if word.startswith('+ '):
            # error word
            added_words.append(word[2:])
        elif word.startswith('- '):
            # error word
            removed_words.append(word[2:])
        else:
            # unchanged
            if added_words or removed_words:
                result.append(
                    f"[{'/'.join(removed_words)} -> {'/'.join(added_words)}]")
                added_words = []
                removed_words = []
            result.append(word[2:])

    if added_words or removed_words:
        result.append(
            f"[{'/'.join(removed_words)} -> {'/'.join(added_words)}]")

    return ' '.join(result)
