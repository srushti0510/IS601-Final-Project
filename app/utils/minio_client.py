import uuid
import io
from fastapi import UploadFile, HTTPException
from minio import Minio
from PIL import Image
from app.dependencies import get_settings
from fastapi import status


settings = get_settings()

minio_client = Minio(
    settings.minio_endpoint.replace("http://", "").replace("https://", ""),
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_endpoint.startswith("https")
)

def resize_image(file: UploadFile, size=(300, 300)) -> io.BytesIO:
    image = Image.open(file.file)
    image = image.convert("RGB")
    image.thumbnail(size)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG", optimize=True)
    img_bytes.seek(0)
    return img_bytes

async def upload_profile_picture(file: UploadFile, user_id: str) -> str:
    try:
        allowed_types = ["image/jpeg", "image/png"]
        if not file.content_type or file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only JPEG and PNG are allowed."
            )

        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset pointer
        
        max_size_bytes = 2 * 1024 * 1024  # 2MB
        if file_size > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum allowed size is 2MB."
            )

        # Process image
        resized_bytes_io = resize_image(file)
        image_data = resized_bytes_io.getvalue()
        image_size = len(image_data)

        # Upload to MinIO
        object_name = f"profile_pictures/{user_id}_{uuid.uuid4()}.jpg"
        minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=object_name,
            data=io.BytesIO(image_data),
            length=image_size,
            content_type="image/jpeg",
        )

        return f"{settings.minio_endpoint}/{settings.minio_bucket}/{object_name}"
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )