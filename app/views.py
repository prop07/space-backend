import uuid
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from app.middleware import ServerRuntimeMiddleware

from .models import Space, Field


def index(request):
    response = ""
    runtime = ServerRuntimeMiddleware.get_server_runtime()
    for key, value in runtime.items():
        response += f'<div style="font-size: 1rem; line-height: 1.5rem; color: rgb(64 64 64); text-transform: capitalize;">{key}: {value}</div>'
    
    return HttpResponse(response)

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def space(request):
    if request.method == "GET":
        unique_value = str(uuid.uuid4())  
        new_space = Space.objects.create(code=unique_value)
        return Response(
            {
                "status": "success",
                "space_code": new_space.code,
                "date": new_space.created_date,
                "message": "Space successfully created."
            },
            status=status.HTTP_201_CREATED
        )

    elif request.method == "POST":
        try:
            space = Space.objects.get(code=request.data.get("space_code"))
            return Response(
                {"status": "success", "message": "Space found.","space_code":request.data.get("space_code")},
                status=status.HTTP_200_OK
            )
        except Space.DoesNotExist:
            return Response(
                {"status": "error", "message": "Invalid space."},
                status=status.HTTP_404_NOT_FOUND
            )

    else:
        return Response(
            {"status": "error", "message": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def field(request, id):
    try:
        space = Space.objects.get(code=id)
        
    except Space.DoesNotExist:
        return Response({"status":"error", "message": "Invalid space."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        try:
            fields = space.field.all().values('field_code', 'title', 'content', 'last_modified')
            return Response({"status":"success","message":"Data retrieved successfully.","fields": list(fields)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message": "Unable to retive data."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "POST":
        try:
            data = request.data
            title = data.get("title")
            content = data.get("content")
            unique_value = str(uuid.uuid4())

            if not title or not content:
                return Response({"status":"error","message": "Title and Content are required."}, status=status.HTTP_400_BAD_REQUEST)

            field = Field.objects.create(
                space_code=space,
                field_code=unique_value,
                title=title,
                content=content
            )
            return Response({
                "status":"success",
                "message": "Added successfully.",
                "field": {
                    "field_code": unique_value,
                    "title": field.title,
                    "content": field.content,
                    "last_modified": field.last_modified
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":"error","message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            data = request.data
            field_code = data.get("field_code")
            if not field_code:
                return Response({"status":"error","message": "Field code is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                field = Field.objects.get(space_code=space, field_code=field_code)
            except Field.DoesNotExist:
                return Response({"status":"error","message": "Field not found or not related to this space."}, status=status.HTTP_404_NOT_FOUND)
                
            if not data.get("title") or not data.get("content"):
                return Response({"status":"error","message": "Title and Content are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Assign values from request data or fallback to existing field values
            title = data.get("title", field.title)
            content = data.get("content", field.content)

            field.title = title
            field.content = content
            field.save()

            return Response({
                "status":"success",
                "message": "Updated successfully.",
                "field": {
                    "field_code": field.field_code,
                    "title": field.title,
                    "content": field.content,
                    "last_modified": field.last_modified
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        try:
            field_code = request.data.get("field_code")
            if not field_code:
                return Response({"status":"error", "message": "Field code is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                field = Field.objects.get(space_code=space, field_code=field_code)
            except Field.DoesNotExist:
                return Response({"status":"error","message": "Field not found or not related to this space."}, status=status.HTTP_404_NOT_FOUND)

            field.delete()
            return Response({"status":"success","message": "Deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":"error","message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"status":"error","message": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



