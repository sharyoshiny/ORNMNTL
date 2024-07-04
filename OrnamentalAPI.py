import requests
import time
from PIL import Image
import io

def check_task_progress(task_id, headers):
    while True:
        response = requests.get(
            f"https://api.meshy.ai/v1/image-to-3d/{task_id}",
            headers=headers,
        )
        response.raise_for_status()
        task_status = response.json()
        status = task_status.get('status')
        progress = task_status.get('progress')

        if status == 'SUCCEEDED':
            print("Task completed.")
            return task_status
        elif status == 'FAILED':
            raise Exception("Task failed.")
        else:
            print(f"Task is {status}. Progress: {progress}%")
            time.sleep(45)  # Wait for 45 seconds before checking again

def process_image_to_3d_mesh(image):
    # Convert the image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)

    # Step 1: Upload the image to a temporary location and get the URL
    files = {'file': ('doodle.png', buffered, 'image/png')}
    upload_response = requests.post(
        'https://api.meshy.ai/v1/image-upload',  # Replace with actual endpoint if available
        headers={'Authorization': 'Bearer YOUR_API_KEY'},
        files=files
    )
    upload_response.raise_for_status()
    upload_url = upload_response.json().get('upload_url')

    if not upload_url:
        raise Exception("Failed to upload image")

    # Step 2: Create an Image to 3D task
    payload = {
        "image_url": upload_url,
        "enable_pbr": True,
    }
    headers = {
      "Authorization": "Bearer YOUR_API_KEY"
    }

    response = requests.post(
        "https://api.meshy.ai/v1/image-to-3d",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()

    task_response = response.json()
    task_id = task_response.get('result')

    if not task_id:
        raise Exception("Failed to get task ID")

    print("Task ID:", task_id)

    # Step 3: Continuously check the progress of the task
    task_status = check_task_progress(task_id, headers)

    # Step 4: If the task succeeded, make a GET request to fetch the final result
    if task_status.get('status') == 'SUCCEEDED':
        response = requests.get(
            f"https://api.meshy.ai/v1/image-to-3d/{task_id}",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    return task_status
