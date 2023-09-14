from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Competition, ReferralCode, Team, Member
from django.core.exceptions import ObjectDoesNotExist
# from .gdrive import drive  # Import the configured PyDrive instance
from .custom_storage import MinioStorage
from os.path import join
from django.core.files.base import ContentFile
import base64

# Create your views here.


# @csrf_exempt
# def register_team(request):
#     if request.method == 'POST':
#         body_bytes = request.body
#         body_unicode = body_bytes.decode('utf-8')

#         try:
#             request_data = json.loads(body_unicode)
#         except json.JSONDecodeError:
#             return HttpResponseBadRequest('BAD REQUEST')

#         # new_team = Team(team_name=request_data.teamName, total_team_members=request_data.totalTeamMembers, leader_name=request_data.leaderName,
#         #                 leader_university=request_data.leaderUniversity, leader_major=request_data.leaderMajor, leader_whatsapp_number=request_data.leaderWANumber, leader_email=request_data.leaderEmail, leader_address=request_data.leaderAddress, leader_student_id=request_data.leaderStudentID, leader_active_student_proof=request_data.leaderActiveStudentProof, leader_3x4_photo=request_data.leader3x4Photo, member_1_name=request_data.members[0].Name, member_1_university=request_data.members[0].University, member_1_major=request_data.members[0].Major, member_1_whatsapp_number=request_data.members[0].WANumber, member_1_email=request_data.members[0].Email, member_1_address=request_data.members[0].Address, member_1_student_id=request_data.members[0].StudentID, member_1_active_student_proof=request_data.members[0].ActiveStudentProof, member_1_3x4_photo=request_data.members[0].3x4Photo, member_2_name=request_data.member2Name, member_2_university=request_data.member2University, member_2_major=request_data.member2Major, member_2_whatsapp_number=request_data.member2WANumber, member_2_email=request_data.member2Email, member_2_address=request_data.member2Address, member_2_student_id=request_data.member2StudentID, member_2_active_student_proof=request_data.member2ActiveStudentProof, member_2_3x4_photo=request_data.member23x4Photo, member_3_name=request_data.member3Name, member_3_university=request_data.member3University, member_3_major=request_data.member3Major, member_3_whatsapp_number=request_data.member3WANumber, member_3_email=request_data.member3Email, member_3_address=request_data.member3Address, member_3_student_id=request_data.member3StudentID, member_3_active_student_proof=request_data.member3ActiveStudentProof, member_3_3x4_photo=request_data.member33x4Photo, payment_total=request_data.paymentTotal, referral_code=request_data.referralCode, payment_methods=request_data.paymentMethods, payment_proof=request_data.paymentProof)

#         new_team = Team(team_name=request_data["teamName"], payment_total=request_data["totalPayment"], referral_code=request_data["referralCode"],
#                         payment_methods=request_data["paymentMethod"], payment_proof=request_data["paymentProof"])
#         # new_team.save()

#         for member in request_data['members']:
#             new_member = Member(name=member['name'], team_id=new_team, role=member['role'], university=member['university'], major=member['major'], whatsapp_number=member['WANumber'], email=member['email'],
#                                 address=member['address'], student_id=member['studentID'], active_student_proof=member['activeStudentProof'], photo_3x4=member['photo3x4'], photo_twibbon=member['photoTwibbon'])
#             # new_member.save()

#         # return JsonResponse(request_data)
#         return HttpResponse('Success!')
#     else:
#         return HttpResponseBadRequest('ONLY POST')


@csrf_exempt
def register_multipart(request):
    if request.method == 'POST':
        # uploaded_files = request.FILES.getlist('foto')

        # json_file = json.loads(request.FILES.get('jsonFile'))
        request_data = json.loads(request.POST['jsonFile'])
        try:
            request_data = json.loads(request.POST['jsonFile'])
            # print(json.loads(request.FILES['jsonFile']))
            # json_content =
            # request_data = json.loads(request.POST['jsonFile'])
        except:
            return JsonResponse({"message": 'BAD REQUEST', "statusCode": 400}, status=400)

        print('helo')
        additional_message = ''

        if "referralCode" in request_data and request_data['referralCode']:
            try:
                referral_code = ReferralCode.objects.get(
                    code=request_data["referralCode"])

                if (referral_code.is_redeemed):
                    # additional_message += 'Referral code sudah digunakan.'
                    return JsonResponse({"message": "Referral code sudah digunakan.", "statusCode": 406}, status=406)
                else:
                    referral_code.is_redeemed = True
                    request_data['referralCode'] = referral_code
                    referral_code.save()
            except ObjectDoesNotExist:
                # additional_message += 'Referral code yang anda masukkan tidak tersedia.'
                return JsonResponse({"message": "Referral code yang anda masukkan tidak tersedia.", "statusCode": 404}, status=404)
            except Exception as e:
                print(e)
                # additional_message += 'Referral code tidak bisa digunakan.'
                return JsonResponse({"message": 'Referral code tidak bisa digunakan.', "statusCode": 500}, status=500)
        else:
            request_data['referralCode'] = ''

        print('one')
        if 'competition' in request_data:
            try:
                competition = Competition.objects.get(
                    name=request_data['competition'])
                min_capacity = competition.min_capacity
                max_capacity = competition.max_capacity
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Unknown competition.", "statusCode": 404}, status=404)
            except Exception as e:
                print(e)
                return JsonResponse({"message": 'Internal server error.', "statusCode": 500}, status=500)
        else:
            return JsonResponse({"message": 'Field competition is empty.', "statusCode": 400}, status=400)

        try:
            # check if the team is already exist
            query_team = Team.objects.get(team_name=request_data['teamName'])
            return JsonResponse({"message": "Team is already exist", "statusCode": 409}, status=409)
        except Exception as e:
            pass

        print('two')
        members = request_data['members']
        if (len(members) < min_capacity or len(members) > max_capacity):
            if (min_capacity == max_capacity):
                return JsonResponse({"message": f'Jumlah anggota tim harus {min_capacity} (termasuk leader).', "statusCode": 400}, status=400)

            return JsonResponse({"message": f'Jumlah anggota tim harus berada di antara {min_capacity} dan {max_capacity} (termasuk leader).', "statusCode": 400}, status=400)

        # payment
        print('three')
        # payment_proof = json.loads(request.POST['paymentProof'])
        print('four')
        # print(payment_proof['base64'])
        # payment_content = ContentFile(
        #     base64.b64decode(payment_proof['base64']))
        # payment_content.name = f'payment.{payment_proof["ext"]}'
        # payment_content.content_type = payment_proof['contentType']
        print('five')

        new_team = Team(team_name=request_data["teamName"], competition=competition, payment_total=request_data["totalPayment"], referral_code=request_data["referralCode"],
                        payment_methods=request_data["paymentMethod"])
        new_team.save()
        # new_team.payment_proof.save(
        #     f'payment.{payment_proof["ext"]}', payment_content)
        ids = {"teamId": new_team.team_id, "memberIds": []}

        for i in range(len(members)):
            if (i == 0):
                key = 'leader'
            else:
                key = f'member{i}'

            # student id
            # member_student_id = json.loads(request.POST[f'{key}KTM'])
            # student_id_content = ContentFile(
            #     base64.b64decode(member_student_id['base64']))
            # student_id_content.content_type = member_student_id['contentType']

            # active student proof
            # member_active_student_proof = json.loads(
            #     request.POST[f'{key}Active'])
            # active_student_proof_content = ContentFile(
            #     base64.b64decode(member_active_student_proof['base64']))
            # active_student_proof_content.content_type = member_active_student_proof[
            #     'contentType']

            # photo 3x4
            # member_photo_3x4 = json.loads(request.POST[f'{key}3x4'])
            # photo_3x4_content = ContentFile(
            #     base64.b64decode(member_photo_3x4['base64']))
            # photo_3x4_content.content_type = member_photo_3x4['contentType']

            # twibbon
            # member_photo_twibbon = json.loads(request.POST[f'{key}Twibbon'])
            # photo_twibbon_content = ContentFile(
            #     base64.b64decode(member_photo_twibbon['base64']))
            # photo_twibbon_content.content_type = member_photo_twibbon['contentType']

            new_member = Member(name=members[i]['name'], team_id=new_team, role=members[i]['role'], university=members[i]['university'], major=members[i]['major'], whatsapp_number=members[i]['WANumber'], email=members[i]['email'],
                                address=members[i]['address'])

            # content_files = [student_id_content, active_student_proof_content,
            #                  photo_3x4_content, photo_twibbon_content]
            # exts = [member_student_id['ext'], member_active_student_proof['ext'],
            #         member_photo_3x4['ext'], member_photo_twibbon['ext']]
            # new_member.save_image_files(content_files, exts)
            new_member.save()
            ids['memberIds'].append(new_member.member_id)

        return JsonResponse({"message": f'Sukses mendaftarkan tim!', "statusCode": 201, "ids": ids}, status=201)
    else:
        return JsonResponse({"message": 'ONLY POST', "statusCode": 400}, status=400)


def get_uploads(request, team_name, filename):
    # return HttpResponse(f'tes\n{team_name}\n{filename}')
    minio_storage = MinioStorage()
    # print(dir(minio_storage))
    file_path = f'uploads/{team_name.replace("%20", " ")}/{filename.replace("%20", " ")}'
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


@csrf_exempt
def register_team_payment(request, team_id):
    if request.method == 'POST':
        try:
            payment_proof = request.FILES.get('paymentProof')

            registered_team = Team.objects.get(team_id=team_id)
            registered_team.save_payment_img(payment_proof)
            return JsonResponse({"message": "Success upload team images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:  # TODO: tambah exception doesn exist
            return JsonResponse({"message": "Cannot find team.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the payment photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)


@csrf_exempt
def register_member_ktm(request, member_id):
    if request.method == 'POST':
        try:
            ktm = request.FILES.get('memberKTM')

            registered_member = Member.objects.get(member_id=member_id)
            registered_member.save_ktm_img(ktm)
            return JsonResponse({"message": "Success upload member images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Cannot find member.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the 'Student ID (KTM)' photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)


@csrf_exempt
def register_member_active(request, member_id):
    if request.method == 'POST':
        try:
            aktif = request.FILES.get('memberActive')

            registered_member = Member.objects.get(member_id=member_id)
            registered_member.save_active_img(aktif)
            return JsonResponse({"message": "Success upload member images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Cannot find member.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the 'Bukti Mahasiswa Aktif' photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)


@csrf_exempt
def register_member_3x4(request, member_id):
    if request.method == 'POST':
        try:
            photo3x4 = request.FILES.get('member3x4')

            registered_member = Member.objects.get(member_id=member_id)
            registered_member.save_3x4_img(photo3x4)
            return JsonResponse({"message": "Success upload member images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Cannot find member.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the '3x4 Photo' photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)


@csrf_exempt
def register_member_follow_instagram(request, member_id):
    if request.method == 'POST':
        try:
            photo_follow_instagram = request.FILES.get('memberFollowInstagram')

            registered_member = Member.objects.get(member_id=member_id)
            registered_member.save_follow_instagram_img(photo_follow_instagram)
            return JsonResponse({"message": "Success upload member images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Cannot find member.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the 'Bukti Follow Instagram ICEE ITB' photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)


@csrf_exempt
def register_member_twibbon(request, member_id):
    if request.method == 'POST':
        try:
            twibbon = request.FILES.get('memberTwibbon')

            registered_member = Member.objects.get(member_id=member_id)
            registered_member.save_twibbon_img(twibbon)
            return JsonResponse({"message": "Success upload member images", "statusCode": 201}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Cannot find member.", "statusCode": 400}, status=400)
        except:
            return JsonResponse({"message": "There is a problem in saving the 'Twibbon' photo.", "statusCode": 500}, status=500)
    else:
        return JsonResponse({"message": "ONLY POST", "statusCode": 400}, status=400)
