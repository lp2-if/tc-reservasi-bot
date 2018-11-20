def follow_message(follower_name):
    message = "Halo " + follower_name + \
            ", terima kasih sudah menambahkan saya sebagai teman.\nSaya dapat membantu anda terkait informasi reservasi ruangan di Departemen Informatika ITS.\n\n"

    return message + help_message()

def help_message():
    command_msg = "Beberapa perintah yang dapat kamu berikan: \n\n"

    command_msg += "1. !today\nUntuk melihat ruangan yang tersedia\n"
    command_msg += "2. !today <nama_ruang>\nUntuk melihat jadwal kegiatan di ruangan tersebut untuk hari ini\n"
    command_msg += "3. !status <nama_kamu>\nUntuk mengecek status reservasi kamu\n\n"
    command_msg += "4. !help\nUntuk mengetahui perintah yang tersedia\n\n"
    command_msg += "Hubungi admin LP2 untuk tambahan fitur"

    return command_msg

def join_message():
    message = "Halo teman - teman semua,\n"
    message += "Terima kasih sudah mengundang saya ke grup ini.\n\n"
    message += "Kirimkan pesan !help untuk melihat perintah yang tersedia.\n\n"
    message += "Have a nice and productive day :D"

    return message