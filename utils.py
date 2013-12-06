def normalize_patches(patches):
    """Normalizes a patch - subracts mean and divides by l1 norm."""
    out = patches - patches.mean(axis=1)[:,None]
    out /= abs(patches).sum(axis=1)[:,None] + .001
    return out
