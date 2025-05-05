from fastapi import UploadFile
import uuid

def upload_profile_picture(file: UploadFile, user_id: str) -> str:
    """
    Uploads a profile picture to Minio and returns the file URL.
    """
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    object_name = f"profile_pictures/{user_id}_{uuid.uuid4()}.{file_extension}"

    # Upload to Minio
    minio_client.put_object(
        bucket_name=settings.minio_bucket,
        object_name=object_name,
        data=file.file,
        length=-1,  # This is required if using streaming
        part_size=10 * 1024 * 1024,  # 10MB chunks
        content_type=file.content_type,
    )

    # Return public URL
    return f"{settings.minio_endpoint}/{settings.minio_bucket}/{object_name}"
