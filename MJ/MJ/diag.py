import sys, os
sys.path.insert(0, os.getcwd())

log = open('diag.log', 'w', encoding='utf-8', buffering=1)

def L(msg):
    log.write(msg + '\n')
    log.flush()

L('[1] start')

mods = [
    'Tools.manage_windows',
    'Tools.search_web',
    'Tools.send_whatsapp_message',
    'Tools.system_power_action',
    'Tools.type_user_message_auto',
    'Tools.write_in_notepad',
    'Tools.desktop_control',
    'Tools.scroll_content',
    'Tools.code_handler',
    'Tools.file_searching',
    'Tools.press_key',
    'Tools.open_app',
    'Tools.scan_system_for_viruses',
    'Tools.time_volume_bright',
    'Tools.multi_task',
    'Tools.generate_ai_image',
    'Tools.code_generator',
    'Tools.news_provider',
    'Tools.youtube_videos',
    'Tools.reminder',
    'Tools.screen_short',
    'Tools.pdf_reader',
    'Tools.send_media_whatsapp',
    'Tools.excel_data_entery',
    'Tools.word_to_pdf',
    'Tools.create_folder',
    'Tools.read_screen_text',
    'Tools.camera_analysis',
    'Tools.screen_analyzer',
    'Tools.image_analysis',
    'Tools.spotify',
]

import importlib
for mod in mods:
    L(f'Trying: {mod}')
    try:
        importlib.import_module(mod)
        L(f'  OK: {mod}')
    except Exception as e:
        import traceback
        L(f'  FAIL: {mod} -> {e}')
        L(traceback.format_exc())

L('[DONE] All tested')
log.close()
