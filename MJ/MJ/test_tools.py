import sys
from PyQt5.QtWidgets import QApplication

tools = [
    'Tools.manage_windows', 'Tools.search_web', 'Tools.send_whatsapp_message',
    'Tools.system_power_action', 'Tools.type_user_message_auto', 'Tools.write_in_notepad',
    'Tools.desktop_control', 'Tools.scroll_content', 'Tools.code_handler',
    'Tools.file_searching', 'Tools.press_key', 'Tools.open_app',
    'Tools.scan_system_for_viruses', 'Tools.time_volume_bright', 'Tools.multi_task',
    'Tools.generate_ai_image', 'Tools.code_generator', 'Tools.news_provider',
    'Tools.youtube_videos', 'Tools.reminder', 'Tools.screen_short',
    'Tools.pdf_reader', 'Tools.send_media_whatsapp', 'Tools.excel_data_entery',
    'Tools.word_to_pdf', 'Tools.create_folder', 'Tools.read_screen_text',
    'Tools.camera_analysis', 'Tools.screen_analyzer', 'Tools.image_analysis',
    'Tools.spotify'
]

f = open('diag10.log', 'w')
f.write('START\n'); f.flush()

import importlib
for t in tools:
    f.write(t + '\n'); f.flush()
    try:
        importlib.import_module(t)
        f.write(t + ' OK\n'); f.flush()
    except BaseException as e:
        f.write(t + ' ERROR ' + str(e) + '\n'); f.flush()
f.write('ALL DONE\n'); f.flush()
f.close()
