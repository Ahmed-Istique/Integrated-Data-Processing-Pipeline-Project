
import requests
import os
from contextlib import closing

# -----------------------------
# Configuration
# -----------------------------
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
SAVE_PATH = 'F:/AI Lab experiment lab/experiment 1/'
# -----------------------------
# Download functions
# -----------------------------
def download_image(img_url, filename):
    """Download a single image"""
    try:
        with closing(requests.get(img_url, headers=HEADERS, stream=True)) as resp:
            resp.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in resp.iter_content(128):
                    f.write(chunk)
        print(f"✓ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def download_multiple_images(num_images=10):
    """Download multiple random images from Picsum"""
    # Create save directory
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        print(f"Created directory: {SAVE_PATH}")
    
    success_count = 0
    for i in range(1, num_images + 1):
        # Picsum provides random images with different dimensions
        img_url = f"https://picsum.photos/800/600?random={i}"
        filename = f"{SAVE_PATH}image_{i}.jpg"
        
        if download_image(img_url, filename):
            success_count += 1
    print(f"\n🎉 Successfully downloaded {success_count}/{num_images} images!")
    print(f"📍 Saved to: {SAVE_PATH}")
# -----------------------------
# Main function
# -----------------------------
def main():
    print("Random Image Downloader")
    print("=" * 30)
    download_multiple_images(10)

if __name__ == "__main__":
    main()

