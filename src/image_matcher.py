@torch.no_grad()
def find_best(
    self,
    text: str
) -> Optional[tuple]:

    if not self.image_data:
        return None

    text = text.lower()

    keywords = [
        "room",
        "suite",
        "bed",
        "bathroom",
        "pool",
        "restaurant",
        "dining",
        "breakfast",
        "bar",
        "spa",
        "gym",
        "beach",
        "ocean",
        "sea",
        "balcony",
        "lobby",
        "view",
    ]

    boosted = []

    for word in keywords:

        if word in text:
            boosted.append(word)

    if boosted:
        text = " ".join(boosted) + " " + text

    candidates = self.find_top_k(
        text=text,
        k=20,
        min_score=0.12
    )

    if not candidates:
        return None

    if len(self.used_images) >= len(self.image_data):
        self.used_images.clear()

    available = [
        item
        for item in candidates
        if item[0] not in self.used_images
    ]

    if not available:
        available = candidates

    image_path, score = available[0]

    self.used_images.add(image_path)
    self.recent_images.append(image_path)

    return (
        image_path,
        score
    )