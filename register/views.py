from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Competition, ReferralCode, Team, Member
from django.core.exceptions import ObjectDoesNotExist
# from .gdrive import drive  # Import the configured PyDrive instance
from .custom_storage import MinioStorage
from os.path import join

# Create your views here.


@csrf_exempt
def register_team(request):
    if request.method == 'POST':
        body_bytes = request.body
        body_unicode = body_bytes.decode('utf-8')

        try:
            request_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('BAD REQUEST')

        # new_team = Team(team_name=request_data.teamName, total_team_members=request_data.totalTeamMembers, leader_name=request_data.leaderName,
        #                 leader_university=request_data.leaderUniversity, leader_major=request_data.leaderMajor, leader_whatsapp_number=request_data.leaderWANumber, leader_email=request_data.leaderEmail, leader_address=request_data.leaderAddress, leader_student_id=request_data.leaderStudentID, leader_active_student_proof=request_data.leaderActiveStudentProof, leader_3x4_photo=request_data.leader3x4Photo, member_1_name=request_data.members[0].Name, member_1_university=request_data.members[0].University, member_1_major=request_data.members[0].Major, member_1_whatsapp_number=request_data.members[0].WANumber, member_1_email=request_data.members[0].Email, member_1_address=request_data.members[0].Address, member_1_student_id=request_data.members[0].StudentID, member_1_active_student_proof=request_data.members[0].ActiveStudentProof, member_1_3x4_photo=request_data.members[0].3x4Photo, member_2_name=request_data.member2Name, member_2_university=request_data.member2University, member_2_major=request_data.member2Major, member_2_whatsapp_number=request_data.member2WANumber, member_2_email=request_data.member2Email, member_2_address=request_data.member2Address, member_2_student_id=request_data.member2StudentID, member_2_active_student_proof=request_data.member2ActiveStudentProof, member_2_3x4_photo=request_data.member23x4Photo, member_3_name=request_data.member3Name, member_3_university=request_data.member3University, member_3_major=request_data.member3Major, member_3_whatsapp_number=request_data.member3WANumber, member_3_email=request_data.member3Email, member_3_address=request_data.member3Address, member_3_student_id=request_data.member3StudentID, member_3_active_student_proof=request_data.member3ActiveStudentProof, member_3_3x4_photo=request_data.member33x4Photo, payment_total=request_data.paymentTotal, referral_code=request_data.referralCode, payment_methods=request_data.paymentMethods, payment_proof=request_data.paymentProof)

        new_team = Team(team_name=request_data["teamName"], payment_total=request_data["totalPayment"], referral_code=request_data["referralCode"],
                        payment_methods=request_data["paymentMethod"], payment_proof=request_data["paymentProof"])
        # new_team.save()

        for member in request_data['members']:
            new_member = Member(name=member['name'], team_id=new_team, role=member['role'], university=member['university'], major=member['major'], whatsapp_number=member['WANumber'], email=member['email'],
                                address=member['address'], student_id=member['studentID'], active_student_proof=member['activeStudentProof'], photo_3x4=member['photo3x4'], photo_twibbon=member['photoTwibbon'])
            # new_member.save()

        # return JsonResponse(request_data)
        return HttpResponse('Success!')
    else:
        return HttpResponseBadRequest('ONLY POST')


@csrf_exempt
def register_multipart(request):
    if request.method == 'POST':
        # uploaded_files = request.FILES.getlist('foto')

        # json_file = json.loads(request.FILES.get('jsonFile'))
        try:
            request_data = json.loads(request.POST['jsonFile'])
            # print(json.loads(request.FILES['jsonFile']))
            # json_content =
            # request_data = json.loads(request.POST['jsonFile'])
        except:
            return JsonResponse({"error": 'BAD REQUEST'}, status=400)

        print('helo')

        payment_proof = request.FILES.get('paymentProof')

        if "referralCode" in request_data:
            try:
                referral_code = ReferralCode.objects.get(
                    code=request_data["referralCode"])

                if (referral_code.is_redeemed):
                    return JsonResponse({"error": "Token is already used."}, status=406)
                else:
                    referral_code.is_redeemed = True
                    request_data['referralCode'] = referral_code
                    referral_code.save()
            # except ObjectDoesNotExist:
            #     return JsonResponse({"error": "Token is not exist."}, status=404)
            except Exception as e:
                print(e)
                pass
                # return JsonResponse({'error': 'Internal server error.'}, status=500)
        else:
            request_data['referralCode'] = ''

        if 'competition' in request_data:
            try:
                competition = Competition.objects.get(
                    name=request_data['competition'])
                min_capacity = competition.min_capacity
                max_capacity = competition.max_capacity
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Unknown competition."}, status=404)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'Internal server error.'}, status=500)
        else:
            return JsonResponse({'error': 'Field competition is empty.'}, status=400)

        try:
            # check if the team is already exist
            query_team = Team.objects.get(team_name=request_data['teamName'])
            return JsonResponse({"error": "Team is already exist"}, status=409)
        except Exception as e:
            pass

        members = request_data['members']
        if (len(members) < min_capacity or len(members) > max_capacity):
            if (min_capacity == max_capacity):
                return JsonResponse({'error': f'Number of team should be {min_capacity}'})

            return JsonResponse({"error": f'Number of team should be between {min_capacity} and {max_capacity}.'}, status=400)

        new_team = Team(team_name=request_data["teamName"], competition=competition, payment_total=request_data["totalPayment"], referral_code=request_data["referralCode"],
                        payment_methods=request_data["paymentMethod"], payment_proof=payment_proof)
        new_team.save()

        for i in range(len(members)):
            if (i == 0):
                key = 'leader'
            else:
                key = f'member{i}'

            member_student_id = request.FILES.get(f'{key}KTM')
            member_active_student_proof = request.FILES.get(f'{key}Active')
            member_photo_3x4 = request.FILES.get(f'{key}3x4')
            member_photo_twibbon = request.FILES.get(f'{key}Twibbon')

            new_member = Member(name=members[i]['name'], team_id=new_team, role=members[i]['role'], university=members[i]['university'], major=members[i]['major'], whatsapp_number=members[i]['WANumber'], email=members[i]['email'],
                                address=members[i]['address'], student_id=member_student_id, active_student_proof=member_active_student_proof, photo_3x4=member_photo_3x4, photo_twibbon=member_photo_twibbon)
            new_member.save()

        return JsonResponse({"message": 'Success created team!'}, status=200)
    else:
        return JsonResponse({"message": 'ONLY POST'}, status=400)


def get_uploads(request, team_name, filename):
    return HttpResponse('hello')
    minio_storage = MinioStorage()
    # print(dir(minio_storage))
    file_path = f'uploads/{team_name}/{filename}'
    print(f'HIHIII {file_path}')
    file = minio_storage.open(name=file_path)

    content_type = 'image/*'
    ext = filename.split(".")[1]
    if ext == 'png':
        content_type = 'image/png'
    elif ext in ['jpg', 'jpeg']:
        content_type = 'image/jpeg'

    response = FileResponse(file)
    response['Content-Type'] = content_type

    return response
    # return HttpResponse('hello')

    # try:
    #     file = minio_storage.open(name=file_path)
    #     return FileResponse(file)
    # except Exception as e:
    #     print(e)
    #     return JsonResponse({'error': 'File not found'}, status=404)

    # file = open(f'uploads/{team_name}/{filename}', 'rb')
    # return FileResponse(file)


# @csrf_exempt
# def upload_to_google_drive(request):
#     if request.method == 'POST' and request.FILES:
#         uploaded_file = request.FILES['file']
#         file_title = uploaded_file.name

#         # Upload the file to Google Drive
#         gdrive_file = drive.CreateFile({'title': file_title})
#         gdrive_file.Upload()

#         return JsonResponse({'message': f'File "{file_title}" uploaded to Google Drive successfully.'})

#     return HttpResponseBadRequest('ERROR')
