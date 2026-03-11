# Relatório consolidado

Este relatório consolida as saídas brutas da suíte de QA.

## 02_pylint.txt
```text
************* Module main
main.py:11:0: C0413: Import "from ui.main_window import LaserflixMainWindow" should be placed at the top of the module (wrong-import-position)
main.py:12:0: C0413: Import "from utils.logging_setup import LOGGER" should be placed at the top of the module (wrong-import-position)
main.py:20:11: W0718: Catching too general exception Exception (broad-exception-caught)
main.py:18:8: W0612: Unused variable 'app' (unused-variable)
************* Module ai.analysis_manager
ai\analysis_manager.py:23:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:26:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:40:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:44:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:50:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:64:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:67:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:69:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:73:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:76:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:78:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:88:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:91:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:99:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:112:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:116:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:121:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:126:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:128:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:131:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:139:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:142:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:150:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:152:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:154:13: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:155:27: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:171:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:174:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:179:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:183:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:186:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:193:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:199:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:204:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:208:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:211:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:216:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:219:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:222:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:226:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:232:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:234:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:239:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:244:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:247:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:250:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:254:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:258:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:260:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:267:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:282:0: C0303: Trailing whitespace (trailing-whitespace)
ai\analysis_manager.py:16:0: R0902: Too many instance attributes (14/7) (too-many-instance-attributes)
ai\analysis_manager.py:143:19: W0718: Catching too general exception Exception (broad-exception-caught)
ai\analysis_manager.py:240:23: W0718: Catching too general exception Exception (broad-exception-caught)
ai\analysis_manager.py:153:4: R0915: Too many statements (53/50) (too-many-statements)
************* Module ai.fallbacks
ai\fallbacks.py:58:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:63:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:70:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:74:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:234:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:240:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:246:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:252:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:366:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:373:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:384:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:395:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:406:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:417:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:421:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:432:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:443:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:454:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:465:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:473:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:476:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:522:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:544:0: C0303: Trailing whitespace (trailing-whitespace)
ai\fallbacks.py:155:8: C0103: Variable name "DATE_VALS" doesn't conform to snake_case naming style (invalid-name)
ai\fallbacks.py:156:8: C0103: Variable name "FUNC_VALS" doesn't conform to snake_case naming style (invalid-name)
ai\fallbacks.py:157:8: C0103: Variable name "ENV_VALS" doesn't conform to snake_case naming style (invalid-name)
ai\fallbacks.py:187:4: R0912: Too many branches (17/12) (too-many-branches)
ai\fallbacks.py:346:4: R0914: Too many local variables (18/15) (too-many-locals)
ai\fallbacks.py:346:35: W0613: Unused argument 'project_path' (unused-argument)
ai\fallbacks.py:346:63: W0613: Unused argument 'structure' (unused-argument)
ai\fallbacks.py:361:8: W0612: Unused variable 'name_norm' (unused-variable)
************* Module ai.image_analyzer
ai\image_analyzer.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:24:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:40:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:49:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:54:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:64:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:71:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:76:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:83:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:93:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:103:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:116:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:129:0: C0303: Trailing whitespace (trailing-whitespace)
ai\image_analyzer.py:25:4: R0914: Too many local variables (18/15) (too-many-locals)
ai\image_analyzer.py:84:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module ai.keyword_maps
ai\keyword_maps.py:663:17: W0109: Duplicate key 'Gamer' in dictionary (duplicate-key)
************* Module ai.ollama_client
ai\ollama_client.py:69:0: C0301: Line too long (104/100) (line-too-long)
ai\ollama_client.py:193:0: C0301: Line too long (107/100) (line-too-long)
ai\ollama_client.py:21:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
ai\ollama_client.py:80:15: W0718: Catching too general exception Exception (broad-exception-caught)
ai\ollama_client.py:150:19: W0718: Catching too general exception Exception (broad-exception-caught)
ai\ollama_client.py:217:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module ai.text_generator
ai\text_generator.py:97:0: C0301: Line too long (105/100) (line-too-long)
ai\text_generator.py:297:0: C0301: Line too long (101/100) (line-too-long)
ai\text_generator.py:300:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:307:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:315:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:325:0: C0301: Line too long (108/100) (line-too-long)
ai\text_generator.py:326:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:354:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:360:0: C0303: Trailing whitespace (trailing-whitespace)
ai\text_generator.py:43:4: R0914: Too many local variables (21/15) (too-many-locals)
ai\text_generator.py:211:15: W0718: Catching too general exception Exception (broad-exception-caught)
ai\text_generator.py:77:37: C0321: More than one statement on a single line (multiple-statements)
ai\text_generator.py:78:37: C0321: More than one statement on a single line (multiple-statements)
ai\text_generator.py:79:37: C0321: More than one statement on a single line (multiple-statements)
ai\text_generator.py:80:37: C0321: More than one statement on a single line (multiple-statements)
ai\text_generator.py:199:20: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
ai\text_generator.py:208:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
ai\text_generator.py:43:4: R0912: Too many branches (15/12) (too-many-branches)
ai\text_generator.py:371:15: W0718: Catching too general exception Exception (broad-exception-caught)
ai\text_generator.py:394:8: C0415: Import outside toplevel (config.constants.FILE_EXTENSIONS) (import-outside-toplevel)
ai\text_generator.py:400:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module config.ui_constants
config\ui_constants.py:134:1: W0511: TODO: Resolver import circular e usar fonte �nica (fixme)
************* Module core.collections_manager
core\collections_manager.py:75:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\collections_manager.py:95:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module core.database
core\database.py:142:0: C0301: Line too long (102/100) (line-too-long)
core\database.py:120:19: W0718: Catching too general exception Exception (broad-exception-caught)
core\database.py:169:19: W0718: Catching too general exception Exception (broad-exception-caught)
core\database.py:139:16: W0612: Unused variable 'path' (unused-variable)
************* Module core.database_controller
core\database_controller.py:22:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:27:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:31:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:40:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:65:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:67:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:80:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:90:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:94:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:98:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:104:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:108:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:116:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:120:0: C0303: Trailing whitespace (trailing-whitespace)
core\database_controller.py:50:19: W0718: Catching too general exception Exception (broad-exception-caught)
core\database_controller.py:74:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\database_controller.py:109:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module core.project_scanner
core\project_scanner.py:15:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:19:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:26:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:31:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:35:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:39:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:43:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:59:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:65:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:67:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:75:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:82:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:85:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:103:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:107:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:112:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:115:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:118:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:128:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:134:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:137:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:139:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:146:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:150:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:153:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:156:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:162:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:168:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:170:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:176:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:181:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
core\project_scanner.py:60:19: W0718: Catching too general exception Exception (broad-exception-caught)
core\project_scanner.py:83:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\project_scanner.py:76:12: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core\project_scanner.py:135:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module core.thumbnail_cache
core\thumbnail_cache.py:36:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:67:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:69:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:84:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:86:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:91:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:229:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_cache.py:89:23: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:81:39: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:61:12: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
core\thumbnail_cache.py:110:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:129:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:134:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core\thumbnail_cache.py:151:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:168:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:182:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:226:27: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_cache.py:249:15: W0718: Catching too general exception Exception (broad-exception-caught)
************* Module core.thumbnail_preloader
core\thumbnail_preloader.py:76:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:82:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:86:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:120:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:123:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:133:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:137:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:145:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:149:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:152:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:176:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:184:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:208:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:212:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:215:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:217:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:237:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:246:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:266:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:273:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:293:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:298:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:325:0: C0303: Trailing whitespace (trailing-whitespace)
core\thumbnail_preloader.py:88:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\thumbnail_preloader.py:150:19: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_preloader.py:151:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\thumbnail_preloader.py:218:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_preloader.py:219:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\thumbnail_preloader.py:244:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\thumbnail_preloader.py:302:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\thumbnail_preloader.py:24:0: W0611: Unused import queue (unused-import)
core\thumbnail_preloader.py:26:0: W0611: Unused as_completed imported from concurrent.futures (unused-import)
************* Module core.virtual_scroll_manager
core\virtual_scroll_manager.py:75:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:81:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:85:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:90:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:92:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:95:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:114:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:118:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:121:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:124:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:128:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:160:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:163:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:165:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:171:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:174:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:177:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:180:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:184:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:188:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:190:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:194:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:196:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:199:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:202:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:219:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:234:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:238:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:242:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:245:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:248:38: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:249:29: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:250:29: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:251:20: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:254:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:266:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:269:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:273:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:284:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:288:0: C0303: Trailing whitespace (trailing-whitespace)
core\virtual_scroll_manager.py:28:0: R0902: Too many instance attributes (18/7) (too-many-instance-attributes)
core\virtual_scroll_manager.py:48:4: R0913: Too many arguments (10/5) (too-many-arguments)
core\virtual_scroll_manager.py:48:4: R0917: Too many positional arguments (10/5) (too-many-positional-arguments)
core\virtual_scroll_manager.py:133:15: W0718: Catching too general exception Exception (broad-exception-caught)
core\virtual_scroll_manager.py:129:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\virtual_scroll_manager.py:134:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\virtual_scroll_manager.py:139:32: W0613: Unused argument 'event' (unused-argument)
core\virtual_scroll_manager.py:24:0: W0611: Unused Optional imported from typing (unused-import)
************* Module core.performance.filter_cache
core\performance\filter_cache.py:45:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:58:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:66:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:71:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:96:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:106:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:115:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:119:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:124:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:129:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:133:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:135:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:157:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:163:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:166:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:172:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:178:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:189:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:197:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\filter_cache.py:68:8: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:102:16: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core\performance\filter_cache.py:107:20: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:114:20: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:128:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:130:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:155:16: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
core\performance\filter_cache.py:167:12: W1203: Use lazy % formatting in logging functions (logging-fstring-interpolation)
************* Module core.performance.predictive_preloader
core\performance\predictive_preloader.py:43:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:56:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:62:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:67:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:93:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:100:0: C0303: Trailing whitespace (trailing-whitespace)
core\performance\predictive_preloader.py:103:0: C0303: Trailing whitespace (trailing-whitespace)

```

## 02_ruff.txt
```text
I001 [*] Import block is un-sorted or un-formatted
 --> QA\12_enforce_quality_gate.py:1:1
  |
1 | / from pathlib import Path
2 | | import sys
  | |__________^
3 |
4 |   reports = Path("QA/reports")
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
 --> QA\13_detect_duplication.py:1:1
  |
1 | / from __future__ import annotations
2 | |
3 | | from collections import defaultdict
4 | | from pathlib import Path
5 | | import hashlib
  | |______________^
6 |
7 |   ROOTS = ["ai", "config", "core", "ui", "utils"]
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> ai\analysis_manager.py:7:1
   |
 5 |   S-05: Thread watchdog para timeout automático (120s)
 6 |   """
 7 | / import os
 8 | | import threading
 9 | | import time
10 | | from typing import Callable, Optional, List, Dict, Any
11 | |
12 | | from config.settings import FAST_MODEL_THRESHOLD
13 | | from utils.logging_setup import LOGGER
   | |______________________________________^
   |
help: Organize imports

UP035 [*] Import from `collections.abc` instead: `Callable`
  --> ai\analysis_manager.py:10:1
   |
 8 | import threading
 9 | import time
10 | from typing import Callable, Optional, List, Dict, Any
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |
12 | from config.settings import FAST_MODEL_THRESHOLD
   |
help: Import from `collections.abc`

UP035 `typing.List` is deprecated, use `list` instead
  --> ai\analysis_manager.py:10:1
   |
 8 | import threading
 9 | import time
10 | from typing import Callable, Optional, List, Dict, Any
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |
12 | from config.settings import FAST_MODEL_THRESHOLD
   |

UP035 `typing.Dict` is deprecated, use `dict` instead
  --> ai\analysis_manager.py:10:1
   |
 8 | import threading
 9 | import time
10 | from typing import Callable, Optional, List, Dict, Any
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 |
12 | from config.settings import FAST_MODEL_THRESHOLD
   |

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:46:38
   |
45 |         # S-05: Watchdog state
46 |         self._current_project_start: Optional[float] = None
   |                                      ^^^^^^^^^^^^^^^
47 |         self._current_project_path: Optional[str] = None
48 |         self._watchdog_thread: Optional[threading.Thread] = None
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:47:37
   |
45 |         # S-05: Watchdog state
46 |         self._current_project_start: Optional[float] = None
47 |         self._current_project_path: Optional[str] = None
   |                                     ^^^^^^^^^^^^^
48 |         self._watchdog_thread: Optional[threading.Thread] = None
49 |         self._watchdog_active = False
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:48:32
   |
46 |         self._current_project_start: Optional[float] = None
47 |         self._current_project_path: Optional[str] = None
48 |         self._watchdog_thread: Optional[threading.Thread] = None
   |                                ^^^^^^^^^^^^^^^^^^^^^^^^^^
49 |         self._watchdog_active = False
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:52:27
   |
51 |         # Callbacks (conecta com UI)
52 |         self.on_progress: Optional[Callable[[int, int, str], None]] = None
   |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
53 |         self.on_start: Optional[Callable[[], None]] = None
54 |         self.on_complete: Optional[Callable[[int, int], None]] = None
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:53:24
   |
51 |         # Callbacks (conecta com UI)
52 |         self.on_progress: Optional[Callable[[int, int, str], None]] = None
53 |         self.on_start: Optional[Callable[[], None]] = None
   |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
54 |         self.on_complete: Optional[Callable[[int, int], None]] = None
55 |         self.on_error: Optional[Callable[[str], None]] = None
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:54:27
   |
52 |         self.on_progress: Optional[Callable[[int, int, str], None]] = None
53 |         self.on_start: Optional[Callable[[], None]] = None
54 |         self.on_complete: Optional[Callable[[int, int], None]] = None
   |                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
55 |         self.on_error: Optional[Callable[[str], None]] = None
   |
help: Convert to `X | None`

UP045 [*] Use `X | None` for type annotations
  --> ai\analysis_manager.py:55:24
   |
53 |         self.on_start: Optional[Callable[[], None]] = None
54 |         self.on_complete: Optional[Callable[[int, int], None]] = None
55 |         self.on_error: Optional[Callable[[str], None]] = None
   |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
56 |     
57 |     def _start_watchdog(self, project_path: str) -> None:
   |
help: Convert to `X | None`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> ai\analysis_manager.py:100:59
    |
 98 |         self._current_project_path = None
 99 |     
100 |     def analyze_single(self, project_path: str, database: Dict[str, Any]) -> None:
    |                                                           ^^^^
101 |         """
102 |         Analisa um único projeto.
    |
help: Replace with `dict`

UP006 [*] Use `list` instead of `List` for type annotation
   --> ai\analysis_manager.py:155:18
    |
153 |     def analyze_batch(
154 |         self, 
155 |         targets: List[str], 
    |                  ^^^^
156 |         database: Dict[str, Any],
157 |         filter_analyzed: bool = False
    |
help: Replace with `list`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> ai\analysis_manager.py:156:19
    |
154 |         self, 
155 |         targets: List[str], 
156 |         database: Dict[str, Any],
    |                   ^^^^
157 |         filter_analyzed: bool = False
158 |     ) -> None:
    |
help: Replace with `dict`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> ai\analysis_manager.py:268:49
    |
266 |         self.logger.info("Solicitado parada da análise")
267 |     
268 |     def get_unanalyzed_projects(self, database: Dict[str, Any]) -> List[str]:
    |                                                 ^^^^
269 |         """
270 |         Retorna lista de projetos não analisados.
    |
help: Replace with `dict`

UP006 [*] Use `list` instead of `List` for type annotation
   --> ai\analysis_manager.py:268:68
    |
266 |         self.logger.info("Solicitado parada da análise")
267 |     
268 |     def get_unanalyzed_projects(self, database: Dict[str, Any]) -> List[str]:
    |                                                                    ^^^^
269 |         """
270 |         Retorna lista de projetos não analisados.
    |
help: Replace with `list`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> ai\analysis_manager.py:283:42
    |
281 |         ]
282 |     
283 |     def get_all_projects(self, database: Dict[str, Any]) -> List[str]:
    |                                          ^^^^
284 |         """
285 |         Retorna lista de todos os projetos válidos.
    |
help: Replace with `dict`

UP006 [*] Use `list` instead of `List` for type annotation
   --> ai\analysis_manager.py:283:61
    |
281 |         ]
282 |     
283 |     def get_all_projects(self, database: Dict[str, Any]) -> List[str]:
    |                                                             ^^^^
284 |         """
285 |         Retorna lista de todos os projetos válidos.
    |
help: Replace with `list`

I001 [*] Import block is un-sorted or un-formatted
  --> ai\fallbacks.py:19:1
   |
17 |     - Novas funções: Book Nook, Tracker, Régua, Organizador de Ferramentas
18 |   """
19 | / import os
20 | | import re
21 | | from utils.logging_setup import LOGGER
22 | | from utils.text_utils import normalize_project_name, remove_accents
23 | | from config.constants import BANNED_STRINGS
24 | |
25 | | from ai.keyword_maps import (
26 | |     DATE_MAP, FUNCTION_MAP, AMBIENTE_MAP,
27 | |     THEME_MAP, STYLE_MAP, PUBLIC_MAP,
28 | |     TRANSLATION_MAP, GENERIC_FALLBACK_FUNCTION,
29 | |     DATE_INFER_MAP,
30 | |     FINAL_FALLBACK_FUNCTION, FINAL_FALLBACK_AMBIENTE,
31 | | )
   | |_^
   |
help: Organize imports

F841 Local variable `name_norm` is assigned to but never used
   --> ai\fallbacks.py:361:9
    |
359 |         raw_name   = project_data.get("name", "Sem nome")
360 |         clean_name = self._clean_name(raw_name)
361 |         name_norm  = normalize_project_name(raw_name)
    |         ^^^^^^^^^
362 |
363 |         tags       = project_data.get("tags", [])
    |
help: Remove assignment to unused variable `name_norm`

I001 [*] Import block is un-sorted or un-formatted
 --> ai\image_analyzer.py:4:1
  |
2 |   Análise de qualidade de imagem e integração com visão
3 |   """
4 | / import os
5 | | from PIL import Image, ImageStat
6 | | from config.settings import IMAGE_QUALITY_THRESHOLDS
7 | | from utils.logging_setup import LOGGER
  | |______________________________________^
  |
help: Organize imports

F601 Dictionary key literal `"Gamer"` repeated
   --> ai\keyword_maps.py:717:5
    |
715 |     "Gastrônomo":       "Aniversário",
716 |     "Músico":           "Aniversário",
717 |     "Gamer":            "Aniversário",
    |     ^^^^^^^
718 |     "Dono de Pet":      "Dia do Animal",
719 |     "Empresas":         "Aniversário Corporativo",
    |
help: Remove repeated key literal `"Gamer"`

I001 [*] Import block is un-sorted or un-formatted
  --> ai\ollama_client.py:5:1
   |
 3 |   v4.0.1: Atualizado para suportar qwen3.5:4b multimodal
 4 |   """
 5 | / import time
 6 | | import base64
 7 | | import io
 8 | | import requests
 9 | | from PIL import Image
10 | | from config.settings import (
11 | |     OLLAMA_BASE_URL,
12 | |     OLLAMA_RETRIES,
13 | |     OLLAMA_HEALTH_TIMEOUT,
14 | |     OLLAMA_HEALTH_CACHE_TTL,
15 | |     OLLAMA_MODELS,
16 | |     TIMEOUTS,
17 | | )
18 | | from utils.logging_setup import LOGGER
   | |______________________________________^
   |
help: Organize imports

E501 Line too long (104 > 100)
  --> ai\ollama_client.py:69:101
   |
67 |             cached = self._health_cache
68 |
69 |             if cached.get("ok") is not None and (now - cached.get("ts", 0.0)) < OLLAMA_HEALTH_CACHE_TTL:
   |                                                                                                     ^^^^
70 |                 return bool(cached["ok"])
   |

E501 Line too long (107 > 100)
   --> ai\ollama_client.py:193:101
    |
191 |                         "role": "user",
192 |                         "content": (
193 |                             "Olhe apenas para o objeto de madeira cortado a laser no centro desta imagem. "
    |                                                                                                     ^^^^^^^
194 |                             "Ignore o fundo, paredes, brinquedos de pelúcia e textos sobrepostos. "
195 |                             "Descreva APENAS o objeto central: seu formato, tema e estilo. "
    |

I001 [*] Import block is un-sorted or un-formatted
  --> ai\text_generator.py:7:1
   |
 5 |   HOT-11: FIX CRÍTICO - Prompt exige 10+ categorias (não 3-5)
 6 |   """
 7 | / import os
 8 | | import re
 9 | | from config.settings import FAST_MODEL_THRESHOLD
10 | | from utils.logging_setup import LOGGER
   | |______________________________________^
   |
help: Organize imports

E701 Multiple statements on one line (colon)
  --> ai\text_generator.py:77:36
   |
75 |             # Contexto técnico
76 |             tech_context = []
77 |             if structure["has_svg"]: tech_context.append("SVG vetorial")
   |                                    ^
78 |             if structure["has_pdf"]: tech_context.append("PDF")
79 |             if structure["has_dxf"]: tech_context.append("DXF/CAD")
   |

E701 Multiple statements on one line (colon)
  --> ai\text_generator.py:78:36
   |
76 |             tech_context = []
77 |             if structure["has_svg"]: tech_context.append("SVG vetorial")
78 |             if structure["has_pdf"]: tech_context.append("PDF")
   |                                    ^
79 |             if structure["has_dxf"]: tech_context.append("DXF/CAD")
80 |             if structure["has_ai"]:  tech_context.append("Adobe Illustrator")
   |

E701 Multiple statements on one line (colon)
  --> ai\text_generator.py:79:36
   |
77 |             if structure["has_svg"]: tech_context.append("SVG vetorial")
78 |             if structure["has_pdf"]: tech_context.append("PDF")
79 |             if structure["has_dxf"]: tech_context.append("DXF/CAD")
   |                                    ^
80 |             if structure["has_ai"]:  tech_context.append("Adobe Illustrator")
81 |             tech_str = ", ".join(tech_context) if tech_context else "formatos variados"
   |

E701 Multiple statements on one line (colon)
  --> ai\text_generator.py:80:35
   |
78 |             if structure["has_pdf"]: tech_context.append("PDF")
79 |             if structure["has_dxf"]: tech_context.append("DXF/CAD")
80 |             if structure["has_ai"]:  tech_context.append("Adobe Illustrator")
   |                                   ^
81 |             tech_str = ", ".join(tech_context) if tech_context else "formatos variados"
   |

E501 Line too long (105 > 100)
  --> ai\text_generator.py:97:101
   |
95 |             # HOT-11: PROMPT REFINADO - EXIGE 10+ CATEGORIAS!
96 |             # ═══════════════════════════════════════════════════════════════
97 |             prompt = f"""Analise este produto de corte laser e responda EXATAMENTE no formato solicitado.
   |                                                                                                     ^^^^^
98 |
99 | 📁 NOME: {name}
   |

E501 Line too long (127 > 100)
   --> ai\text_generator.py:153:101
    |
152 | ### FORMATO DE RESPOSTA (siga exatamente):
153 | Categorias: [cat1], [cat2], [cat3], [cat4], [cat5], [cat6], [cat7], [cat8], [cat9], [cat10], [cat11 opcional], [cat12 opcional]
    |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
154 | Tags: [tag1], [tag2], [tag3], [tag4], [tag5], [tag6], [tag7], [tag8], [tag9], [tag10]
    |

E501 Line too long (101 > 100)
   --> ai\text_generator.py:297:101
    |
295 |             prompt = (
296 |                 "Você é especialista em peças físicas de corte a laser — placas, espelhos, "
297 |                 "porta-retratos, tabuletas, cabides, calendários, nomes decorativos e similares.\n\n"
    |                                                                                                     ^
298 |                 "NOME DA PEÇA (use isso como verdade absoluta sobre o que é o produto): "
299 |                 + clean_name + vision_context + "\n\n"
    |

E501 Line too long (108 > 100)
   --> ai\text_generator.py:325:101
    |
323 | …     "Nunca use frases genéricas que servem para qualquer produto.]\n\n"
324 | …     "💖 Perfeito Para:\n"
325 | …     "[2 a 3 frases práticas com exemplos reais de uso e ocasião para ESTA peça específica.]\n\n"
    |                                                                                           ^^^^^^^^
326 | …     
327 | …     # ────────────────────────────────────────────────────────────
    |

I001 [*] Import block is un-sorted or un-formatted
  --> backup_manager.py:7:1
   |
 5 |   """
 6 |
 7 | / import os
 8 | | import shutil
 9 | | import json
10 | | from datetime import datetime
11 | | from pathlib import Path
12 | | from typing import List, Dict, Optional
13 | | import hashlib
   | |______________^
   |
help: Organize imports

UP035 `typing.List` is deprecated, use `list` instead
  --> backup_manager.py:12:1
   |
10 | from datetime import datetime
11 | from pathlib import Path
12 | from typing import List, Dict, Optional
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
13 | import hashlib
   |

UP035 `typing.Dict` is deprecated, use `dict` instead
  --> backup_manager.py:12:1
   |
10 | from datetime import datetime
11 | from pathlib import Path
12 | from typing import List, Dict, Optional
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
13 | import hashlib
   |

UP006 [*] Use `list` instead of `List` for type annotation
  --> backup_manager.py:50:33
   |
48 |             self._save_metadata([])
49 |     
50 |     def _load_metadata(self) -> List[Dict]:
   |                                 ^^^^
51 |         """Carrega metadados dos backups"""
52 |         try:
   |
help: Replace with `list`

UP006 [*] Use `dict` instead of `Dict` for type annotation
  --> backup_manager.py:50:38
   |
48 |             self._save_metadata([])
49 |     
50 |     def _load_metadata(self) -> List[Dict]:
   |                                      ^^^^
51 |         """Carrega metadados dos backups"""
52 |         try:
   |
help: Replace with `dict`

UP015 [*] Unnecessary mode argument
  --> backup_manager.py:53:43
   |
51 |         """Carrega metadados dos backups"""
52 |         try:
53 |             with open(self.metadata_file, 'r', encoding='utf-8') as f:
   |                                           ^^^
54 |                 return json.load(f)
55 |         except:
   |
help: Remove mode argument

E722 Do not use bare `except`
  --> backup_manager.py:55:9
   |
53 |             with open(self.metadata_file, 'r', encoding='utf-8') as f:
54 |                 return json.load(f)
55 |         except:
   |         ^^^^^^
56 |             return []
   |

UP006 [*] Use `list` instead of `List` for type annotation
  --> backup_manager.py:58:40
   |
56 |             return []
57 |     
58 |     def _save_metadata(self, metadata: List[Dict]):
   |                                        ^^^^
59 |         """Salva metadados dos backups"""
60 |         with open(self.metadata_file, 'w', encoding='utf-8') as f:
   |
help: Replace with `list`

UP006 [*] Use `dict` instead of `Dict` for type annotation
  --> backup_manager.py:58:45
   |
56 |             return []
57 |     
58 |     def _save_metadata(self, metadata: List[Dict]):
   |                                             ^^^^
59 |         """Salva metadados dos backups"""
60 |         with open(self.metadata_file, 'w', encoding='utf-8') as f:
   |
help: Replace with `dict`

E722 Do not use bare `except`
  --> backup_manager.py:83:17
   |
81 |                     with open(filepath, 'rb') as f:
82 |                         hasher.update(f.read())
83 |                 except:
   |                 ^^^^^^
84 |                     pass
   |

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> backup_manager.py:108:55
    |
106 |         return False
107 |     
108 |     def create_backup(self, description: str = "") -> Dict:
    |                                                       ^^^^
109 |         """
110 |         Cria novo backup do estado atual
    |
help: Replace with `dict`

UP006 [*] Use `list` instead of `List` for type annotation
   --> backup_manager.py:170:31
    |
168 |         return backup_info
169 |     
170 |     def list_backups(self) -> List[Dict]:
    |                               ^^^^
171 |         """Lista todos os backups disponíveis"""
172 |         return self._load_metadata()
    |
help: Replace with `list`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> backup_manager.py:170:36
    |
168 |         return backup_info
169 |     
170 |     def list_backups(self) -> List[Dict]:
    |                                    ^^^^
171 |         """Lista todos os backups disponíveis"""
172 |         return self._load_metadata()
    |
help: Replace with `dict`

UP045 [*] Use `X | None` for type annotations
   --> backup_manager.py:235:57
    |
233 |         return True
234 |     
235 |     def get_backup_info(self, backup_index: int = 0) -> Optional[Dict]:
    |                                                         ^^^^^^^^^^^^^^
236 |         """Retorna informações de um backup específico"""
237 |         metadata = self._load_metadata()
    |
help: Convert to `X | None`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> backup_manager.py:235:66
    |
233 |         return True
234 |     
235 |     def get_backup_info(self, backup_index: int = 0) -> Optional[Dict]:
    |                                                                  ^^^^
236 |         """Retorna informações de um backup específico"""
237 |         metadata = self._load_metadata()
    |
help: Replace with `dict`

B007 Loop control variable `dirs` not used within loop body
   --> backup_manager.py:265:19
    |
263 |         """Calcula tamanho total do diretório em bytes"""
264 |         total = 0
265 |         for root, dirs, files in os.walk(path):
    |                   ^^^^
266 |             for file in files:
267 |                 filepath = Path(root) / file
    |
help: Rename unused `dirs` to `_dirs`

E722 Do not use bare `except`
   --> backup_manager.py:270:17
    |
268 |                 try:
269 |                     total += filepath.stat().st_size
270 |                 except:
    |                 ^^^^^^
271 |                     pass
272 |         return total
    |

F541 [*] f-string without any placeholders
   --> backup_manager.py:331:19
    |
329 |         backup = manager.get_backup_info(index)
330 |         if backup:
331 |             print(f"\n⚠️ ATENÇÃO: Você vai restaurar o backup:")
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
332 |             print(f"📅 Data: {backup['datetime']}")
333 |             print(f"📝 Descrição: {backup['description'] or '(sem descrição)'}")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> backup_manager.py:334:19
    |
332 |             print(f"📅 Data: {backup['datetime']}")
333 |             print(f"📝 Descrição: {backup['description'] or '(sem descrição)'}")
334 |             print(f"\n🚨 O estado atual será substituído!")
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
335 |             
336 |             confirm = input("\nDigite 'SIM' para confirmar: ")
    |
help: Remove extraneous `f` prefix

F541 [*] f-string without any placeholders
   --> backup_manager.py:364:19
    |
362 |         backup = manager.get_backup_info(index)
363 |         if backup:
364 |             print(f"\n⚠️ Você vai deletar o backup:")
    |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
365 |             print(f"📅 Data: {backup['datetime']}")
    |
help: Remove extraneous `f` prefix

I001 [*] Import block is un-sorted or un-formatted
 --> config\settings.py:4:1
  |
2 |   Configurações centralizadas do Laserflix v4.0.1.3
3 |   """
4 | / from __future__ import annotations
5 | | import os
  | |_________^
6 |
7 |   # Diretório raiz do projeto (pasta onde este arquivo está, um nível acima de config/)
  |
help: Organize imports

I001 [*] Import block is un-sorted or un-formatted
  --> core\collections_manager.py:13:1
   |
11 |   - file_path injetável no __init__ (testabilidade, DIP)
12 |   """
13 | / from __future__ import annotations
14 | |
15 | | import json
16 | | import os
17 | | from typing import Dict, List, Set
18 | | from config.settings import DB_FILE
19 | | from utils.logging_setup import LOGGER
   | |______________________________________^
   |
help: Organize imports

UP035 `typing.Dict` is deprecated, use `dict` instead
  --> core\collections_manager.py:17:1
   |
15 | import json
16 | import os
17 | from typing import Dict, List, Set
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
18 | from config.settings import DB_FILE
19 | from utils.logging_setup import LOGGER
   |

UP035 `typing.List` is deprecated, use `list` instead
  --> core\collections_manager.py:17:1
   |
15 | import json
16 | import os
17 | from typing import Dict, List, Set
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
18 | from config.settings import DB_FILE
19 | from utils.logging_setup import LOGGER
   |

UP035 `typing.Set` is deprecated, use `set` instead
  --> core\collections_manager.py:17:1
   |
15 | import json
16 | import os
17 | from typing import Dict, List, Set
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
18 | from config.settings import DB_FILE
19 | from utils.logging_setup import LOGGER
   |

UP006 [*] Use `dict` instead of `Dict` for type annotation
  --> core\collections_manager.py:46:27
   |
44 |     def __init__(self, file_path: str | None = None) -> None:
45 |         self.file_path: str = file_path or COLLECTIONS_FILE
46 |         self.collections: Dict[str, List[str]] = {}
   |                           ^^^^
47 |         self.logger = LOGGER
48 |         self.load()
   |
help: Replace with `dict`

UP006 [*] Use `list` instead of `List` for type annotation
  --> core\collections_manager.py:46:37
   |
44 |     def __init__(self, file_path: str | None = None) -> None:
45 |         self.file_path: str = file_path or COLLECTIONS_FILE
46 |         self.collections: Dict[str, List[str]] = {}
   |                                     ^^^^
47 |         self.logger = LOGGER
48 |         self.load()
   |
help: Replace with `list`

UP015 [*] Unnecessary mode argument
  --> core\collections_manager.py:61:39
   |
60 |         try:
61 |             with open(self.file_path, "r", encoding="utf-8") as f:
   |                                       ^^^
62 |                 self.collections = json.load(f)
63 |             self.logger.info(
   |
help: Remove mode argument

UP006 [*] Use `list` instead of `List` for type annotation
   --> core\collections_manager.py:176:38
    |
174 |         return True
175 |
176 |     def get_all_collections(self) -> List[str]:
    |                                      ^^^^
177 |         """Retorna lista de nomes de coleções (ordenada)."""
178 |         return sorted(self.collections.keys())
    |
help: Replace with `list`

UP006 [*] Use `list` instead of `List` for type annotation
   --> core\collections_manager.py:232:53
    |
230 |         return True
231 |
232 |     def get_projects(self, collection_name: str) -> List[str]:
    |                                                     ^^^^
233 |         """Retorna lista de paths de projetos na coleção."""
234 |         return self.collections.get(collection_name, [])
    |
help: Replace with `list`

UP006 [*] Use `list` instead of `List` for type annotation
   --> core\collections_manager.py:236:64
    |
234 |         return self.collections.get(collection_name, [])
235 |
236 |     def get_collection_projects(self, collection_name: str) -> List[str]:
    |                                                                ^^^^
237 |         """Alias para get_projects() (compatibilidade com UI)."""
238 |         return self.get_projects(collection_name)
    |
help: Replace with `list`

UP006 [*] Use `list` instead of `List` for type annotation
   --> core\collections_manager.py:240:61
    |
238 |         return self.get_projects(collection_name)
239 |
240 |     def get_project_collections(self, project_path: str) -> List[str]:
    |                                                             ^^^^
241 |         """Retorna lista de coleções que contêm o projeto (ordenada)."""
242 |         return sorted([
    |
help: Replace with `list`

UP006 [*] Use `set` instead of `Set` for type annotation
   --> core\collections_manager.py:253:50
    |
251 |     # === Utilitários ===
252 |
253 |     def clean_orphan_projects(self, valid_paths: Set[str]) -> int:
    |                                                  ^^^
254 |         """
255 |         Remove referências a projetos que não existem mais.
    |
help: Replace with `set`

UP006 [*] Use `dict` instead of `Dict` for type annotation
   --> core\collections_manager.py:279:28
    |
277 |         return removed_count
278 |
279 |     def get_stats(self) -> Dict[str, int]:
    |                            ^^^^
280 |         """Retorna estatísticas do sistema de coleções."""
281 |         total_projects = sum(len(paths) for paths in self.collections.values())
    |
help: Replace with `dict`

I001 [*] Import block is un-sorted or un-formatted
  --> core\database.py:4:1
   |
 2 |   Gerenciamento de banco de dados JSON
 3 |   """
 4 | / from __future__ import annotations
 5 | |
 6 | | import json
 7 | | import os
 8 | | import shutil
 9 | | from datetime import datetime
10 | | from typing import Any, Iterator
11 | | from config.settings import DB_FILE, CONFIG_FILE, BACKUP_FOLDER, MAX_AUTO_BACKUPS
12 | | from utils.logging_setup import LOGGER
   | |______________________________________^
   |
help: Organize imports

UP035 [*] Import from `collections.abc` instead: `Iterator`
  --> core\database.py:10:1
   |
 8 | import shutil
 9 | from datetime import datetime
10 | from typing import Any, Iterator
   | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 | from config.settings import DB_FILE, CONFIG_FILE, BACKUP_FOLDER, MAX_AUTO_BACKUPS
12 | from utils.logging_setup import LOGGER
   |
help: Import from `collections.abc`

UP015 [*] Unnecessary mode argument
  --> core\database.py:94:41
   |
93 |         try:
94 |             with open(self.config_file, "r", encoding="utf-8") as f:
   |                                         ^^^
95 |                 self.config = json.load(f)
96 |             self.logger.info("✅ Config carregado: %d pastas", len(self.config.get("folders", [])))
   |
help: Remove mode argument

UP015 [*] Unnecessary mode argument
   --> core\database.py:117:45
    |
115 |             )
116 |             try:
117 |                 with open(self.config_file, "r", encoding="latin-1") as f:
    |                                             ^^^
118 |                     self.config = json.load(f)
119 |           
```

## 03_mypy.txt
```text
ui\virtual_scroll.py:41: error: Need type annotation for "items" (hint:
"items: list[<type>] = ...")  [var-annotated]
            self.items        = []  # Lista de (path, data)
            ^~~~~~~~~~
ui\virtual_scroll.py:43: error: Need type annotation for "visible_rows" (hint:
"visible_rows: set[<type>] = ...")  [var-annotated]
            self.visible_rows = set()  # Linhas atualmente renderizadas
            ^~~~~~~~~~~~~~~~~
ui\virtual_scroll.py:44: error: Need type annotation for "row_widgets" (hint:
"row_widgets: dict[<type>, <type>] = ...")  [var-annotated]
            self.row_widgets  = {}  # Cache: {row: [widgets]}
            ^~~~~~~~~~~~~~~~
ui\virtual_scroll.py:84: error: Incompatible types in assignment (expression
has type "Callable[..., Any]", variable has type "None")  [assignment]
            self.card_builder = card_builder
                                ^~~~~~~~~~~~
ui\virtual_scroll.py:199: error: "None" not callable  [misc]
                widget = self.card_builder(
                         ^~~~~~~~~~~~~~~~~~
ui\project_card.py:267: error: Cannot infer type of lambda  [misc]
                              command=lambda cc=cat: cb["on_set_category"]...
                                      ^
ui\project_card.py:273: error: Cannot infer type of lambda  [misc]
                b.bind("<Enter>", lambda e, btn=b, dc=dark_clr: btn.config...
                                  ^
ui\project_card.py:274: error: Cannot infer type of lambda  [misc]
                b.bind("<Leave>", lambda e, btn=b, lc=clr: btn.config(bg=l...
                                  ^
ui\project_card.py:283: error: Cannot infer type of lambda  [misc]
                b = tk.Button(tf, text=disp, command=lambda t=tag: cb["on_...
                                                     ^
ui\project_card.py:288: error: Cannot infer type of lambda  [misc]
                b.bind("<Enter>", lambda e, w=b: w.config(bg=ACCENT_RED))
                                  ^
ui\project_card.py:289: error: Cannot infer type of lambda  [misc]
                b.bind("<Leave>", lambda e, w=b: w.config(bg="#3A3A3A"))
                                  ^
ui\project_card.py:297: error: Cannot infer type of lambda  [misc]
                  command=lambda o=origin: cb["on_set_origin"](o)
                          ^
ui\project_card.py:317: error: Cannot infer type of lambda  [misc]
                        command=lambda c=col_name: cb.get("on_set_collecti...
                                ^
ui\project_card.py:329: error: Cannot infer type of lambda  [misc]
                    b.bind("<Enter>", lambda e, bt=b, dc=dark_col: bt.conf...
                                      ^
ui\project_card.py:330: error: Cannot infer type of lambda  [misc]
                    b.bind("<Leave>", lambda e, bt=b: bt.config(bg=COLLECT...
                                      ^
ui\project_card.py:375: error: Cannot infer type of lambda  [misc]
                command=lambda b=btn_good: cb["on_toggle_good"](project_pa...
                        ^
ui\project_card.py:383: error: Cannot infer type of lambda  [misc]
                command=lambda b=btn_bad: cb["on_toggle_bad"](project_path...
                        ^
ui\sidebar.py:63: error: Argument 1 to "_bind_scroll" of "SidebarPanel" has
incompatible type "None"; expected "Widget"  [arg-type]
            self._bind_scroll(self._content)
                              ^~~~~~~~~~~~~
ui\sidebar.py:88: error: Incompatible types in assignment (expression has type
"Canvas", variable has type "None")  [assignment]
            self._canvas = tk.Canvas(container, bg=BG_SECONDARY, highlight...
                           ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~...
ui\sidebar.py:89: error: "None" has no attribute "yview"  [attr-defined]
    ...tk.Scrollbar(container, orient="vertical", command=self._canvas.yview)
                                                          ^~~~~~~~~~~~~~~~~~
ui\sidebar.py:90: error: Incompatible types in assignment (expression has type
"Frame", variable has type "None")  [assignment]
            self._content = tk.Frame(self._canvas, bg=BG_SECONDARY)
                            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:91: error: "None" has no attribute "bind"  [attr-defined]
            self._content.bind(
            ^~~~~~~~~~~~~~~~~~
ui\sidebar.py:93: error: "None" has no attribute "configure"  [attr-defined]
                lambda e: self._canvas.configure(scrollregion=self._canvas...
                          ^~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:93: error: "None" has no attribute "bbox"  [attr-defined]
    ...   lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("al...
                                                        ^~~~~~~~~~~~~~~~~
ui\sidebar.py:95: error: "None" has no attribute "create_window" 
[attr-defined]
            self._canvas.create_window((0, 0), window=self._content, ancho...
            ^~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:96: error: "None" has no attribute "configure"  [attr-defined]
            self._canvas.configure(yscrollcommand=sb.set)
            ^~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:97: error: "None" has no attribute "pack"  [attr-defined]
            self._canvas.pack(side="left", fill="both", expand=True)
            ^~~~~~~~~~~~~~~~~
ui\sidebar.py:99: error: "None" has no attribute "bind"  [attr-defined]
            self._canvas.bind(
            ^~~~~~~~~~~~~~~~~
ui\sidebar.py:101: error: "None" has no attribute "yview_scroll" 
[attr-defined]
                lambda e: self._canvas.yview_scroll(int(-1 * (e.delta / SC...
                          ^~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:126: error: "None" has no attribute "winfo_children" 
[attr-defined]
            for w in self._origins_frame.winfo_children():
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:140: error: Cannot infer type of lambda  [misc]
                btn.config(command=lambda o=origin, b=btn: self._cb["on_or...
                                   ^
ui\sidebar.py:142: error: Cannot infer type of lambda  [misc]
                btn.bind("<Enter>",  lambda e, b=btn: b.config(bg=BG_CARD)...
                                     ^
ui\sidebar.py:143: error: Cannot infer type of lambda  [misc]
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_SECOND...
                                    ^
ui\sidebar.py:144: error: Argument 1 to "_bind_scroll" of "SidebarPanel" has
incompatible type "None"; expected "Widget"  [arg-type]
            self._bind_scroll(self._origins_frame)
                              ^~~~~~~~~~~~~~~~~~~
ui\sidebar.py:152: error: "None" has no attribute "winfo_children" 
[attr-defined]
            for w in self._collections_frame.winfo_children():
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:200: error: "None" has no attribute "winfo_children" 
[attr-defined]
            for w in self._categories_frame.winfo_children():
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:221: error: Cannot infer type of lambda  [misc]
                btn.config(command=lambda c=cat, b=btn: self._cb["on_categ...
                                   ^
ui\sidebar.py:223: error: Cannot infer type of lambda  [misc]
                btn.bind("<Enter>",  lambda e, b=btn: b.config(bg=BG_CARD)...
                                     ^
ui\sidebar.py:224: error: Cannot infer type of lambda  [misc]
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_SECOND...
                                    ^
ui\sidebar.py:233: error: Argument 1 to "_bind_scroll" of "SidebarPanel" has
incompatible type "None"; expected "Widget"  [arg-type]
            self._bind_scroll(self._categories_frame)
                              ^~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:236: error: "None" has no attribute "winfo_children" 
[attr-defined]
            for w in self._tags_frame.winfo_children():
                     ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:257: error: Cannot infer type of lambda  [misc]
                btn.config(command=lambda t=tag, b=btn: self._cb["on_tag"]...
                                   ^
ui\sidebar.py:259: error: Cannot infer type of lambda  [misc]
                btn.bind("<Enter>", lambda e, w=btn: w.config(bg=BG_CARD))
                                    ^
ui\sidebar.py:260: error: Cannot infer type of lambda  [misc]
                btn.bind("<Leave>", lambda e, w=btn: w.config(bg=BG_SECOND...
                                    ^
ui\sidebar.py:261: error: Argument 1 to "_bind_scroll" of "SidebarPanel" has
incompatible type "None"; expected "Widget"  [arg-type]
            self._bind_scroll(self._tags_frame)
                              ^~~~~~~~~~~~~~~~
ui\sidebar.py:270: error: "None" has no attribute "yview_scroll" 
[attr-defined]
                lambda e: self._canvas.yview_scroll(int(-1 * (e.delta / SC...
                          ^~~~~~~~~~~~~~~~~~~~~~~~~
ui\sidebar.py:273: error: Argument 1 to "_bind_scroll" of "SidebarPanel" has
incompatible type "Widget | Toplevel"; expected "Widget"  [arg-type]
                self._bind_scroll(child)
                                  ^~~~~
ui\header.py:50: error: Need type annotation for "filter_btns" (hint:
"filter_btns: dict[<type>, <type>] = ...")  [var-annotated]
            self.filter_btns = {}  # {ftype: btn}
            ^~~~~~~~~~~~~~~~
ui\header.py:90: error: Incompatible types in assignment (expression has type
"Timer", variable has type "None")  [assignment]
            self._search_timer = threading.Timer(0.3, self._cb["on_search"...
                                 ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\header.py:91: error: "None" has no attribute "start"  [attr-defined]
            self._search_timer.start()
            ^~~~~~~~~~~~~~~~~~~~~~~~
ui\header.py:120: error: Cannot infer type of lambda  [misc]
                    command=lambda f=ftype: self._cb["on_filter"](f),
                            ^
ui\header.py:130: error: Cannot infer type of lambda  [misc]
                btn.bind("<Enter>", lambda e, w=btn: w.config(fg=ACCENT_RE...
                                    ^
ui\header.py:132: error: Cannot infer type of lambda  [misc]
                btn.bind("<Leave>", lambda e, w=btn: w.config(bg="#000000"...
                                    ^
ui\edit_modal.py:70: error: Argument 1 to "_build_tag_list" of "EditModal" has
incompatible type "Toplevel"; expected "Widget"  [arg-type]
            self._listbox, _ = self._build_tag_list(win)
                                                    ^~~
utils\recursive_scanner.py:65: error: Returning Any from function declared to
return "list[dict[Any, Any]]"  [no-any-return]
            return self.found_products
            ^~~~~~~~~~~~~~~~~~~~~~~~~~
utils\recursive_scanner.py:81: error: Returning Any from function declared to
return "list[dict[Any, Any]]"  [no-any-return]
            return self.found_products
            ^~~~~~~~~~~~~~~~~~~~~~~~~~
utils\recursive_scanner.py:93: error: Returning Any from function declared to
return "dict[Any, Any]"  [no-any-return]
            return self.stats.copy()
            ^~~~~~~~~~~~~~~~~~~~~~~~
ui\model_settings_dialog.py:17: error: Library stubs not installed for
"requests"  [import-untyped]
    import requests
    ^
ui\duplicate_resolution_dialog.py:28: error: Need type annotation for
"choice_vars" (hint: "choice_vars: dict[<type>, <type>] = ...")  [var-annotated]
            self.choice_vars  = {}
            ^~~~~~~~~~~~~~~~
ui\duplicate_resolution_dialog.py:163: error: Returning Any from function
declared to return "dict[Any, Any] | None"  [no-any-return]
        return dialog.get_result()
        ^~~~~~~~~~~~~~~~~~~~~~~~~~
ui\controllers\analysis_controller.py:50: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ui\controllers\analysis_controller.py:51: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ui\controllers\analysis_controller.py:52: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ui\controllers\analysis_controller.py:53: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ui\controllers\analysis_controller.py:54: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
core\performance\viewport_manager.py:65: error: Need type annotation for
"all_items" (hint: "all_items: list[<type>] = ...")  [var-annotated]
            self.all_items = []  # Lista completa de items
            ^~~~~~~~~~~~~~
core\performance\viewport_manager.py:67: error: Need type annotation for
"rendered_indices" (hint: "rendered_indices: set[<type>] = ...") 
[var-annotated]
            self.rendered_indices = set()  # �ndices j� renderizados
            ^~~~~~~~~~~~~~~~~~~~~
core\performance\viewport_manager.py:68: error: Need type annotation for
"card_widgets" (hint: "card_widgets: dict[<type>, <type>] = ...") 
[var-annotated]
            self.card_widgets = {}  # {index: widget}
            ^~~~~~~~~~~~~~~~~
core\performance\viewport_manager.py:90: error: Incompatible types in
assignment (expression has type
"Callable[[Frame, str, dict[Any, Any], int, int], Widget]", variable has type
"None")  [assignment]
            self.card_builder_fn = card_builder_fn
                                   ^~~~~~~~~~~~~~~
core\performance\viewport_manager.py:162: error: "None" not callable  [misc]
                widget = self.card_builder_fn(
                         ^~~~~~~~~~~~~~~~~~~~~
core\performance\filter_cache.py:60: error: Need type annotation for "cache" 
[var-annotated]
            self.cache = OrderedDict()
            ^~~~~~~~~~
core\performance\filter_cache.py:110: error: Returning Any from function
declared to return "list[Any]"  [no-any-return]
                        return result
                        ^~~~~~~~~~~~~
ai\ollama_client.py:8: error: Library stubs not installed for "requests" 
[import-untyped]
    import requests
    ^
ai\ollama_client.py:8: note: Hint: "python3 -m pip install types-requests"
ai\ollama_client.py:8: note: (or run "mypy --install-types" to install all missing stub packages)
ai\ollama_client.py:8: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
ai\analysis_manager.py:46: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:47: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:48: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:52: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:53: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:54: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ai\analysis_manager.py:55: note: By default the bodies of untyped functions are not checked, consider using --check-untyped-defs  [annotation-unchecked]
ui\managers\dialog_manager.py:96: error: Cannot infer type of lambda  [misc]
                b.bind("<Enter>", lambda e, w=b: w.config(bg=ACCENT_RED))
                                  ^
ui\managers\dialog_manager.py:97: error: Cannot infer type of lambda  [misc]
                b.bind("<Leave>", lambda e, w=b: w.config(bg=BG_CARD))
                                  ^
ui\recursive_import_integration.py:86: error: Need type annotation for
"imported_paths" (hint: "imported_paths: list[<type>] = ...")  [var-annotated]
            self.imported_paths  = []
            ^~~~~~~~~~~~~~~~~~~
ui\recursive_import_integration.py:309: error: Need type annotation for "new"
(hint: "new: list[<type>] = ...")  [var-annotated]
                new, existing  = [], []
                ^~~
ui\recursive_import_integration.py:309: error: Need type annotation for
"existing" (hint: "existing: list[<type>] = ...")  [var-annotated]
                new, existing  = [], []
                     ^~~~~~~~
ui\recursive_import_integration.py:319: error: Incompatible types in assignment
(expression has type "Thread", variable has type "None")  [assignment]
            self.import_thread = threading.Thread(
                                 ^~~~~~~~~~~~~~~~~
ui\recursive_import_integration.py:324: error: "None" has no attribute "start" 
[attr-defined]
            self.import_thread.start()
            ^~~~~~~~~~~~~~~~~~~~~~~~
core\thumbnail_preloader.py:84: error: Need type annotation for "cache" 
[var-annotated]
            self.cache = OrderedDict()
            ^~~~~~~~~~
core\thumbnail_preloader.py:272: error: Returning Any from function declared to
return "PhotoImage | None"  [no-any-return]
                    return cached
                    ^~~~~~~~~~~~~
core\performance\predictive_preloader.py:59: error: Need type annotation for
"preloaded_pages" (hint: "preloaded_pages: set[<type>] = ...")  [var-annotated]
            self.preloaded_pages = set()  # P�ginas j� precarregadas
            ^~~~~~~~~~~~~~~~~~~~
core\performance\predictive_preloader.py:109: error: Incompatible types in
assignment (expression has type "Thread", variable has type "None") 
[assignment]
            self.active_preload_thread = threading.Thread(
                                         ^~~~~~~~~~~~~~~~~
core\performance\predictive_preloader.py:115: error: "None" has no attribute
"start"  [attr-defined]
            self.active_preload_thread.start()
            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ui\controllers\optimized_display_controller.py:293: error: Argument "key" to
"get_or_compute" of "FilterCache" has incompatible type
"tuple[str, str, tuple[Any, ...], str | None, str, tuple[tuple[Any, Any], ...]]";
expected "tuple[str, Any, str]"  [arg-type]
                key=cache_key,
                    ^~~~~~~~~
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Program Files\Python314\Lib\site-packages\mypy\__main__.py", line 37, in <module>
    console_entry()
    ~~~~~~~~~~~~~^^
  File "C:\Program Files\Python314\Lib\site-packages\mypy\__main__.py", line 15, in console_entry
    main()
    ~~~~^^
  File "mypy\main.py", line 135, in main
  File "mypy\main.py", line 219, in run_build
    res = build.build(sources, options, None, flush_errors, fscache, stdout, stderr)
  File "mypy\build.py", line 222, in build
  File "mypy\build.py", line 301, in _build
    graph = dispatch(sources, manager, stdout)
  File "mypy\build.py", line 2952, in dispatch
    process_graph(graph, manager)
  File "mypy\build.py", line 3347, in process_graph
    done, still_working = manager.wait_for_done(graph)
  File "mypy\build.py", line 925, in wait_for_done
    process_stale_scc(graph, next_scc, self)
  File "mypy\build.py", line 3513, in process_stale_scc
    manager.flush_errors(manager.errors.simplify_path(graph[id].xpath), formatted, False)
  File "mypy\main.py", line 211, in flush_errors
    show_messages(new_messages, f, formatter, options)
  File "mypy\main.py", line 254, in show_messages
    f.write(msg + "\n")
  File "C:\Program Files\Python314\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 42-43: character maps to <undefined>
ui\main_window.py:120: error: Need type annotation for "_card_registry" (hint:
"_card_registry: dict[<type>, <type>] = ...")  [var-annotated]
            self._card_registry = {}  # FIX-SELECTION-FLICKER: {path: card...
            ^~~~~~~~~~~~~~~~~~~
ui\main_window.py:144: error: "LaserflixMainWindow" has no attribute
"content_canvas"  [attr-defined]
                canvas=self.content_canvas,
                       ^~~~~~~~~~~~~~~~~~~
ui\main_window.py:145: error: "LaserflixMainWindow" has no attribute
"scrollable_frame"  [attr-defined]
                scrollable_frame=self.scrollable_frame,
                                 ^~~~~~~~~~~~~~~~~~~~~
ui\main_window.py:158: error: "LaserflixMainWindow" has no attribute
"status_bar"  [attr-defined]
    ...analysis_ctrl.on_analysis_complete = lambda msg: self.status_bar.confi...
                                                        ^~~~~~~~~~~~~~~
ui\main_window.py:193: error: "LaserflixMainWindow" has no attribute
"status_bar"  [attr-defined]
    ...ection_dialog_mgr.on_status_update = lambda msg: self.status_bar.confi...
                                                        ^~~~~~~~~~~~~~~
ui\main_window.py:195: error: "LaserflixMainWindow" has no attribute "sidebar" 
[attr-defined]
                self.sidebar.refresh(self.database, self.collections_manag...
                ^~~~~~~~~~~~
ui\main_window.py:196: error: "_invalidate_cache" of "LaserflixMainWindow" does
not return a value (it only ever returns None)  [func-returns-value]
                self._invalidate_cache()
                ^~~~~~~~~~~~~~~~~~~~~~~~
ui\main_window.py:200: error: "LaserflixMainWindow" has no attribute
"progress_bar"; maybe "progress_ui"?  [attr-defined]
                self.progress_bar, self.stop_btn, self.status_bar, self.ro...
                ^~~~~~~~~~~~~~~~~
ui\main_window.py:200: error: "LaserflixMainWindow" has no attribute "stop_btn"
 [attr-defined]
                self.progress_bar, self.stop_btn, self.status_bar, self.ro...
                                   ^~~~~~~~~~~~~
ui\main_window.py:200: error: "LaserflixMainWindow" has no attribute
"status_bar"  [attr-defined]
                self.progress_bar, self.stop_btn, self.status_bar, self.ro...
                                                  ^~~~~~~~~~~~~~~
ui\main_window.py:211: error: "LaserflixMainWindow" has no attribute
"status_bar"  [attr-defined]
                on_status_update=lambda msg: self.status_bar.config(text=m...
                                             ^~~~~~~~~~~~~~~
ui\main_window.py:260: error: Incompatible types in assignment (expression has
type "dict[Any, Any]", variable has type "None")  [assignment]
                self._last_display_state = current_state
                                           ^~~~~~~~~~~~~
ui\main_window.py:279: error: "LaserflixMainWindow" has no attribute "sidebar" 
[attr-defined]
            self.sidebar.refresh(self.database, self.collections_manager)
            ^~~~~~~~~~~~
ui\main_window.py:283: error: "LaserflixMainWindow" has no attribute
"status_bar"  [attr-defined]

```

## 04_radon_cc.txt
```text
main.py
    F 15:0 main - A (2)
ai\analysis_manager.py
    M 153:4 AnalysisManager.analyze_batch - B (9)
    C 16:0 AnalysisManager - A (4)
    M 100:4 AnalysisManager.analyze_single - A (4)
    M 268:4 AnalysisManager.get_unanalyzed_projects - A (4)
    M 57:4 AnalysisManager._start_watchdog - A (3)
    M 283:4 AnalysisManager.get_all_projects - A (3)
    M 27:4 AnalysisManager.__init__ - A (1)
    M 92:4 AnalysisManager._stop_watchdog - A (1)
    M 261:4 AnalysisManager.stop - A (1)
ai\fallbacks.py
    M 187:4 FallbackGenerator._build_categories - E (31)
    M 346:4 FallbackGenerator.fallback_description - C (20)
    M 140:4 FallbackGenerator.fallback_categories - C (13)
    C 78:0 FallbackGenerator - B (10)
    M 316:4 FallbackGenerator._build_tags - B (9)
    F 44:0 _match_all - B (6)
    M 111:4 FallbackGenerator.translate_name - B (6)
    F 34:0 _match - A (4)
    M 547:4 FallbackGenerator._clean_name - A (2)
    M 91:4 FallbackGenerator.__init__ - A (1)
    M 98:4 FallbackGenerator.fallback_analysis - A (1)
    M 262:4 FallbackGenerator._infer_ambiente_from_function - A (1)
ai\image_analyzer.py
    C 10:0 ImageAnalyzer - A (4)
    M 25:4 ImageAnalyzer.quality_score - A (4)
    M 104:4 ImageAnalyzer.analyze_cover - A (4)
    M 94:4 ImageAnalyzer.should_use_vision - A (3)
    M 20:4 ImageAnalyzer.__init__ - A (1)
ai\ollama_client.py
    M 90:4 OllamaClient.generate_text - C (12)
    M 166:4 OllamaClient.describe_image - B (6)
    C 21:0 OllamaClient - A (5)
    M 60:4 OllamaClient.is_available - A (4)
    M 27:4 OllamaClient.__init__ - A (2)
    M 48:4 OllamaClient.update_models - A (1)
    M 84:4 OllamaClient._get_model - A (1)
    M 87:4 OllamaClient._get_timeout - A (1)
ai\text_generator.py
    M 43:4 TextGenerator.analyze_project - D (24)
    M 215:4 TextGenerator.generate_description - B (9)
    C 13:0 TextGenerator - B (7)
    M 392:4 TextGenerator._find_first_image - A (4)
    M 33:4 TextGenerator._choose_model_role - A (2)
    M 385:4 TextGenerator._get_structure - A (2)
    M 404:4 TextGenerator._clean_name - A (2)
    M 26:4 TextGenerator.__init__ - A (1)
core\collections_manager.py
    M 134:4 CollectionsManager.rename_collection - A (5)
    M 253:4 CollectionsManager.clean_orphan_projects - A (5)
    M 50:4 CollectionsManager.load - A (4)
    M 82:4 CollectionsManager.save - A (4)
    M 279:4 CollectionsManager.get_stats - A (4)
    C 25:0 CollectionsManager - A (3)
    M 112:4 CollectionsManager.create_collection - A (3)
    M 186:4 CollectionsManager.add_project - A (3)
    M 209:4 CollectionsManager.remove_project - A (3)
    M 240:4 CollectionsManager.get_project_collections - A (3)
    M 44:4 CollectionsManager.__init__ - A (2)
    M 160:4 CollectionsManager.delete_collection - A (2)
    M 108:4 CollectionsManager.add_collection - A (1)
    M 176:4 CollectionsManager.get_all_collections - A (1)
    M 180:4 CollectionsManager.get_collection_size - A (1)
    M 232:4 CollectionsManager.get_projects - A (1)
    M 236:4 CollectionsManager.get_collection_projects - A (1)
    M 247:4 CollectionsManager.is_project_in_collection - A (1)
core\database.py
    M 127:4 DatabaseManager.load_database - C (11)
    M 178:4 DatabaseManager.auto_backup - B (8)
    M 224:4 DatabaseManager._save_json_atomic - B (8)
    M 84:4 DatabaseManager.load_config - B (6)
    M 259:4 DatabaseManager._try_restore_from_backup - A (5)
    C 15:0 DatabaseManager - A (4)
    M 30:4 DatabaseManager.__init__ - A (3)
    M 205:4 DatabaseManager.manual_backup - A (3)
    M 55:4 DatabaseManager.remove_project - A (2)
    M 47:4 DatabaseManager.get_project - A (1)
    M 51:4 DatabaseManager.set_project - A (1)
    M 62:4 DatabaseManager.has_project - A (1)
    M 66:4 DatabaseManager.all_paths - A (1)
    M 70:4 DatabaseManager.all_projects - A (1)
    M 74:4 DatabaseManager.project_count - A (1)
    M 78:4 DatabaseManager.iter_projects - A (1)
    M 123:4 DatabaseManager.save_config - A (1)
    M 172:4 DatabaseManager.save_database - A (1)
core\database_controller.py
    C 13:0 DatabaseController - A (3)
    M 32:4 DatabaseController.export - A (3)
    M 81:4 DatabaseController.import_from_file - A (3)
    M 57:4 DatabaseController.manual_backup - A (2)
    M 117:4 DatabaseController._notify_status - A (2)
    M 121:4 DatabaseController._notify_changed - A (2)
    M 23:4 DatabaseController.__init__ - A (1)
core\project_scanner.py
    M 86:4 ProjectScanner.analyze_project_structure - C (13)
    M 140:4 ProjectScanner.extract_tags_from_name - C (12)
    C 11:0 ProjectScanner - B (9)
    M 20:4 ProjectScanner.scan_projects - B (8)
    M 68:4 ProjectScanner.get_origin_from_path - A (5)
    M 16:4 ProjectScanner.__init__ - A (1)
core\protocols.py
    C 20:0 RefreshCallback - A (2)
    C 26:0 ModeChangedCallback - A (2)
    C 32:0 ProjectsRemovedCallback - A (2)
    C 38:0 ProgressCallback - A (2)
    C 44:0 DisplayUpdatedCallback - A (2)
    M 22:4 RefreshCallback.__call__ - A (1)
    M 28:4 ModeChangedCallback.__call__ - A (1)
    M 34:4 ProjectsRemovedCallback.__call__ - A (1)
    M 40:4 ProgressCallback.__call__ - A (1)
    M 46:4 DisplayUpdatedCallback.__call__ - A (1)
core\thumbnail_cache.py
    M 198:4 ThumbnailCache.get_cover_image_async - B (7)
    M 124:4 ThumbnailCache.get - B (6)
    M 233:4 ThumbnailCache.get_all_project_images - B (6)
    C 24:0 ThumbnailCache - A (4)
    M 95:4 ThumbnailCache._safe_callback - A (4)
    M 141:4 ThumbnailCache.set - A (4)
    M 172:4 ThumbnailCache.find_first_image - A (4)
    M 114:4 ThumbnailCache.stop - A (3)
    M 154:4 ThumbnailCache.load_thumbnail - A (3)
    M 186:4 ThumbnailCache.get_cover_image - A (2)
    M 257:4 ThumbnailCache.get_stats - A (2)
    M 32:4 ThumbnailCache.__init__ - A (1)
    M 44:4 ThumbnailCache.set_root - A (1)
    M 54:4 ThumbnailCache._start_worker - A (1)
    M 253:4 ThumbnailCache.clear - A (1)
core\thumbnail_preloader.py
    M 93:4 ThumbnailPreloader.preload_batch - B (9)
    M 222:4 ThumbnailPreloader.find_first_image - A (5)
    C 36:0 ThumbnailPreloader - A (4)
    M 155:4 ThumbnailPreloader.preload_single - A (3)
    M 188:4 ThumbnailPreloader._load_thumbnail - A (3)
    M 249:4 ThumbnailPreloader._get_from_cache - A (3)
    M 276:4 ThumbnailPreloader._add_to_cache - A (3)
    M 319:4 ThumbnailPreloader.get_stats - A (2)
    M 61:4 ThumbnailPreloader.__init__ - A (1)
    M 304:4 ThumbnailPreloader.clear_cache - A (1)
    M 312:4 ThumbnailPreloader.shutdown - A (1)
core\virtual_scroll_manager.py
    M 206:4 VirtualScrollManager._recycle_widgets - A (5)
    M 146:4 VirtualScrollManager.update_visible_items - A (4)
    M 223:4 VirtualScrollManager._render_visible_items - A (4)
    C 28:0 VirtualScrollManager - A (3)
    M 100:4 VirtualScrollManager._calculate_viewport - A (3)
    M 277:4 VirtualScrollManager.clear - A (3)
    M 48:4 VirtualScrollManager.__init__ - A (1)
    M 139:4 VirtualScrollManager._on_canvas_resize - A (1)
    M 257:4 VirtualScrollManager.refresh_data - A (1)
    M 293:4 VirtualScrollManager.get_stats - A (1)
core\performance\filter_cache.py
    M 136:4 FilterCache.invalidate - A (5)
    M 72:4 FilterCache.get_or_compute - A (4)
    C 34:0 FilterCache - A (3)
    M 179:4 FilterCache.get_stats - A (2)
    M 46:4 FilterCache.__init__ - A (1)
    M 173:4 FilterCache.invalidate_all - A (1)
    M 198:4 FilterCache.reset_stats - A (1)
core\performance\predictive_preloader.py
    M 68:4 PredictivePreloader.prefetch_next_page - B (6)
    M 122:4 PredictivePreloader._preload_pages_background - B (6)
    C 33:0 PredictivePreloader - A (3)
    M 164:4 PredictivePreloader._cancel_active_preload - A (3)
    M 181:4 PredictivePreloader.on_scroll_progress - A (2)
    M 204:4 PredictivePreloader.get_stats - A (2)
    M 44:4 PredictivePreloader.__init__ - A (1)
    M 173:4 PredictivePreloader.on_filter_changed - A (1)
    M 196:4 PredictivePreloader.clear - A (1)
core\performance\viewport_manager.py
    M 141:4 ViewportManager._render_range - A (4)
    C 33:0 ViewportManager - A (3)
    M 94:4 ViewportManager.render_visible_range - A (3)
    M 173:4 ViewportManager._on_viewport_change - A (2)
    M 191:4 ViewportManager.clear - A (2)
    M 202:4 ViewportManager.get_stats - A (2)
    M 44:4 ViewportManager.__init__ - A (1)
    M 77:4 ViewportManager.set_items - A (1)
    M 184:4 ViewportManager._do_deferred_render - A (1)
ui\collections_dialog.py
    M 280:4 CollectionsDialog._rename_collection - A (5)
    M 343:4 CollectionsDialog._remove_project_from_collection - A (5)
    M 257:4 CollectionsDialog._create_collection - A (4)
    M 313:4 CollectionsDialog._delete_collection - A (4)
    C 27:0 CollectionsDialog - A (3)
    M 207:4 CollectionsDialog._refresh_collections_list - A (2)
    M 224:4 CollectionsDialog._on_collection_select - A (2)
    M 237:4 CollectionsDialog._load_projects - A (2)
    M 35:4 CollectionsDialog.__init__ - A (1)
    M 57:4 CollectionsDialog._build_ui - A (1)
    M 379:4 CollectionsDialog._center - A (1)
ui\duplicate_resolution_dialog.py
    F 155:0 show_duplicate_resolution - A (3)
    M 36:4 DuplicateResolutionDialog._build_ui - A (3)
    C 14:0 DuplicateResolutionDialog - A (2)
    M 101:4 DuplicateResolutionDialog._create_item - A (2)
    M 136:4 DuplicateResolutionDialog._set_all - A (2)
    M 141:4 DuplicateResolutionDialog._confirm - A (2)
    M 15:4 DuplicateResolutionDialog.__init__ - A (1)
    M 146:4 DuplicateResolutionDialog._cancel - A (1)
    M 151:4 DuplicateResolutionDialog.get_result - A (1)
ui\edit_modal.py
    M 110:4 EditModal._add_tag - A (4)
    C 16:0 EditModal - A (3)
    M 84:4 EditModal._build_tag_list - A (3)
    M 120:4 EditModal._save - A (3)
    M 115:4 EditModal._remove_tag - A (2)
    M 24:4 EditModal.__init__ - A (1)
    M 37:4 EditModal._build - A (1)
ui\header.py
    M 53:4 HeaderBar.set_select_btn_active - A (4)
    C 29:0 HeaderBar - A (3)
    M 62:4 HeaderBar.set_active_filter - A (3)
    M 82:4 HeaderBar._debounced_search - A (2)
    M 93:4 HeaderBar._build - A (2)
    M 44:4 HeaderBar.__init__ - A (1)
    M 171:4 HeaderBar._build_colorful_menu - A (1)
ui\import_mode_dialog.py
    M 44:4 ImportModeDialog._build_ui - A (5)
    C 19:0 ImportModeDialog - A (3)
    M 148:4 ImportModeDialog._update_frames - A (3)
    M 156:4 ImportModeDialog._repaint - A (3)
    M 171:4 ImportModeDialog._confirm - A (3)
    F 192:0 show_import_mode_dialog - A (2)
    M 164:4 ImportModeDialog._browse - A (2)
    M 20:4 ImportModeDialog.__init__ - A (1)
    M 183:4 ImportModeDialog._cancel - A (1)
    M 188:4 ImportModeDialog.get_result - A (1)
ui\import_preview_dialog.py
    M 39:4 ImportPreviewDialog._build_ui - B (7)
    C 14:0 ImportPreviewDialog - A (3)
    M 15:4 ImportPreviewDialog.__init__ - A (1)
    M 122:4 ImportPreviewDialog._confirm - A (1)
    M 127:4 ImportPreviewDialog._cancel - A (1)
    M 132:4 ImportPreviewDialog.get_confirmed - A (1)
ui\main_window.py
    M 246:4 LaserflixMainWindow._should_rebuild - B (8)
    M 343:4 LaserflixMainWindow._update_card_selection_visual - B (8)
    M 298:4 LaserflixMainWindow._apply_filter - B (7)
    M 382:4 LaserflixMainWindow.display_projects - B (6)
    M 458:4 LaserflixMainWindow.open_project_modal - A (4)
    M 492:4 LaserflixMainWindow._on_edit_save - A (3)
    C 74:0 LaserflixMainWindow - A (2)
    M 226:4 LaserflixMainWindow.__del__ - A (2)
    M 237:4 LaserflixMainWindow._schedule_viewport_update - A (2)
    M 270:4 LaserflixMainWindow._invalidate_cache - A (2)
    M 329:4 LaserflixMainWindow._on_selection_mode_changed - A (2)
    M 477:4 LaserflixMainWindow._modal_toggle - A (2)
    M 520:4 LaserflixMainWindow.remove_project - A (2)
    M 75:4 LaserflixMainWindow.__init__ - A (1)
    M 230:4 LaserflixMainWindow._build_ui - A (1)
    M 233:4 LaserflixMainWindow._on_scroll - A (1)
    M 243:4 LaserflixMainWindow._update_visible_cards - A (1)
    M 275:4 LaserflixMainWindow._refresh_all - A (1)
    M 281:4 LaserflixMainWindow._on_projects_removed - A (1)
    M 286:4 LaserflixMainWindow._add_filter_chip - A (1)
    M 290:4 LaserflixMainWindow.set_filter - A (1)
    M 295:4 LaserflixMainWindow._on_search - A (1)
    M 316:4 LaserflixMainWindow._on_origin_filter - A (1)
    M 319:4 LaserflixMainWindow._on_category_filter - A (1)
    M 322:4 LaserflixMainWindow._on_tag_filter - A (1)
    M 325:4 LaserflixMainWindow._on_collection_filter - A (1)
    M 339:4 LaserflixMainWindow._on_selection_count_changed - A (1)
    M 369:4 LaserflixMainWindow._on_add_to_collection - A (1)
    M 372:4 LaserflixMainWindow._on_remove_from_collection - A (1)
    M 375:4 LaserflixMainWindow._on_new_collection_with - A (1)
    M 378:4 LaserflixMainWindow.open_collections_dialog - A (1)
    M 418:4 LaserflixMainWindow._get_card_callbacks - A (1)
    M 442:4 LaserflixMainWindow._build_empty_state - A (1)
    M 448:4 LaserflixMainWindow._get_thumbnail_async - A (1)
    M 484:4 LaserflixMainWindow._modal_generate_desc - A (1)
    M 489:4 LaserflixMainWindow.open_edit_mode - A (1)
    M 504:4 LaserflixMainWindow.toggle_favorite - A (1)
    M 508:4 LaserflixMainWindow.toggle_done - A (1)
    M 512:4 LaserflixMainWindow.toggle_good - A (1)
    M 516:4 LaserflixMainWindow.toggle_bad - A (1)
    M 531:4 LaserflixMainWindow.clean_orphans - A (1)
    M 535:4 LaserflixMainWindow.analyze_single_project - A (1)
    M 538:4 LaserflixMainWindow.analyze_only_new - A (1)
    M 541:4 LaserflixMainWindow.reanalyze_all - A (1)
    M 544:4 LaserflixMainWindow.generate_descriptions_for_new - A (1)
    M 547:4 LaserflixMainWindow.generate_descriptions_for_all - A (1)
    M 551:4 LaserflixMainWindow.open_import_dialog - A (1)
    M 555:4 LaserflixMainWindow.open_prepare_folders - A (1)
    M 558:4 LaserflixMainWindow.open_model_settings - A (1)
    M 561:4 LaserflixMainWindow.open_categories_picker - A (1)
    M 564:4 LaserflixMainWindow.export_database - A (1)
    M 567:4 LaserflixMainWindow.import_database - A (1)
    M 570:4 LaserflixMainWindow.manual_backup - A (1)
    M 573:4 LaserflixMainWindow._on_import_complete - A (1)
ui\model_settings_dialog.py
    M 190:4 ModelSettingsDialog._save - B (7)
    M 179:4 ModelSettingsDialog._load_current_values - A (5)
    M 249:4 ModelSettingsDialog._do_test - A (5)
    C 28:0 ModelSettingsDialog - A (3)
    M 220:4 ModelSettingsDialog._restore_defaults - A (3)
    M 66:4 ModelSettingsDialog._build_ui - A (2)
    M 238:4 ModelSettingsDialog._test_connection - A (2)
    M 43:4 ModelSettingsDialog.__init__ - A (1)
    M 167:4 ModelSettingsDialog._section - A (1)
    M 280:4 ModelSettingsDialog._set_status - A (1)
    M 288:4 ModelSettingsDialog._center - A (1)
ui\prepare_folders_dialog.py
    M 164:4 PrepareFoldersDialog._execute - A (5)
    C 17:0 PrepareFoldersDialog - A (4)
    M 146:4 PrepareFoldersDialog._run - A (4)
    M 208:4 PrepareFoldersDialog._close - A (3)
    M 18:4 PrepareFoldersDialog.__init__ - A (2)
    M 43:4 PrepareFoldersDialog._build_ui - A (2)
    M 138:4 PrepareFoldersDialog._browse - A (2)
    M 198:4 PrepareFoldersDialog._log - A (2)
ui\project_card.py
    F 160:0 build_card - E (31)
    F 42:0 _bind_context_menu_recursive - A (3)
    F 66:0 _create_analysis_badge - A (3)
    F 36:0 _darken - A (2)
    F 100:0 _create_context_menu_handler - A (1)
ui\project_modal.py
    M 127:4 ProjectModal._build_left_panel - D (21)
    C 22:0 ProjectModal - B (7)
    M 337:4 ProjectModal._make_toggle - B (6)
    M 320:4 ProjectModal._confirm_remove - A (3)
    M 58:4 ProjectModal.open - A (2)
    M 367:4 ProjectModal._build_right_panel - A (2)
    M 49:4 ProjectModal.__init__ - A (1)
ui\recursive_import_integration.py
    M 92:4 RecursiveImportManager.start_import - D (27)
    M 326:4 RecursiveImportManager._import_loop - B (9)
    M 453:4 RecursiveImportManager._detect_origin - B (8)
    C 58:0 RecursiveImportManager - B (7)
    M 273:4 RecursiveImportManager._scan_simple - A (5)
    M 248:4 RecursiveImportManager._scan_products - A (4)
    M 305:4 RecursiveImportManager._check_existing - A (4)
    M 437:4 RecursiveImportManager._generate_descriptions_batch - A (4)
    M 430:4 RecursiveImportManager._wait_for_analysis_manager - A (2)
    M 67:4 RecursiveImportManager.__init__ - A (1)
    M 317:4 RecursiveImportManager._import_products - A (1)
    M 389:4 RecursiveImportManager._run_sequential_analysis - A (1)
ui\sidebar.py
    M 199:4 SidebarPanel._update_categories - C (11)
    M 146:4 SidebarPanel._update_collections - B (7)
    M 235:4 SidebarPanel._update_tags - B (7)
    M 125:4 SidebarPanel._update_origins - B (6)
    C 22:0 SidebarPanel - A (5)
    M 65:4 SidebarPanel.set_active_btn - A (5)
    M 83:4 SidebarPanel._build - A (2)
    M 267:4 SidebarPanel._bind_scroll - A (2)
    M 33:4 SidebarPanel.__init__ - A (1)
    M 49:4 SidebarPanel.refresh - A (1)
ui\virtual_scroll.py
    M 100:4 VirtualScrollGrid._update_visible_cards - B (8)
    M 210:4 VirtualScrollGrid._destroy_row - A (5)
    M 178:4 VirtualScrollGrid._render_row - A (4)
    C 19:0 VirtualScrollGrid - A (3)
    M 166:4 VirtualScrollGrid._render_initial_cards - A (2)
    M 226:4 VirtualScrollGrid._clear_all_widgets - A (2)
    M 29:4 VirtualScrollGrid.__init__ - A (1)
    M 54:4 VirtualScrollGrid._setup_smooth_scroll - A (1)
    M 75:4 VirtualScrollGrid.update_items - A (1)
    M 237:4 VirtualScrollGrid.refresh - A (1)
    M 244:4 VirtualScrollGrid.scroll_to_top - A (1)
ui\builders\cards_grid_builder.py
    C 20:0 CardsGridBuilder - A (4)
    M 24:4 CardsGridBuilder.build - A (3)
ui\builders\header_builder.py
    M 87:4 HeaderBuilder._build_title - A (5)
    C 19:0 HeaderBuilder - A (4)
    M 23:4 HeaderBuilder.build - A (4)
    M 68:4 HeaderBuilder._build_counter - A (1)
    M 123:4 HeaderBuilder._build_navigation - A (1)
ui\builders\navigation_builder.py
    M 120:4 NavigationBuilder._build_pagination_controls - A (5)
    C 20:0 NavigationBuilder - A (3)
    M 24:4 NavigationBuilder.build - A (1)
    M 44:4 NavigationBuilder._build_sort_controls - A (1)
ui\builders\ui_builder.py
    C 27:0 UIBuilder - A (2)
    M 67:4 UIBuilder._build_main_container - A (2)
    M 31:4 UIBuilder.build - A (1)
    M 45:4 UIBuilder._build_header - A (1)
    M 118:4 UIBuilder._build_status_bar - A (1)
    M 151:4 UIBuilder._bind_keyboard_shortcuts - A (1)
ui\components\chips_bar.py
    M 39:4 ChipsBar.update - C (13)
    C 13:0 ChipsBar - A (3)
    M 164:4 ChipsBar._on_chip_removed - A (2)
    M 169:4 ChipsBar._on_clear_all_clicked - A (2)
    M 23:4 ChipsBar.__init__ - A (1)
    M 125:4 ChipsBar._create_chip - A (1)
    M 174:4 ChipsBar.show - A (1)
    M 178:4 ChipsBar.hide - A (1)
    M 182:4 ChipsBar.is_visible - A (1)
ui\components\selection_bar.py
    C 11:0 SelectionBar - A (2)
    M 112:4 SelectionBar._setup_hover_effects - A (2)
    M 124:4 SelectionBar.update_count - A (2)
    M 146:4 SelectionBar._on_select_all_clicked - A (2)
    M 150:4 SelectionBar._on_deselect_all_clicked - A (2)
    M 154:4 SelectionBar._on_remove_clicked - A (2)
    M 158:4 SelectionBar._on_cancel_clicked - A (2)
    M 20:4 SelectionBar.__init__ - A (1)
    M 133:4 SelectionBar.show - A (1)
    M 137:4 SelectionBar.hide - A (1)
    M 141:4 SelectionBar.is_visible - A (1)
ui\components\status_bar.py
    C 12:0 StatusBar - A (2)
    M 66:4 StatusBar.update_progress - A (2)
    M 13:4 StatusBar.__init__ - A (1)
    M 51:4 StatusBar.set_text - A (1)
    M 55:4 StatusBar.show_progress - A (1)
    M 61:4 StatusBar.hide_progress - A (1)
ui\controllers\analysis_controller.py
    M 159:4 AnalysisController.generate_descriptions_for_new - A (5)
    M 282:4 AnalysisController._on_analysis_done - A (5)
    C 24:0 AnalysisController - A (3)
    M 80:4 AnalysisController.analyze_only_new - A (3)
    M 100:4 AnalysisController.reanalyze_all - A (3)
    M 182:4 AnalysisController.generate_descriptions_for_all - A (3)
    M 131:4 AnalysisController.generate_description_single - A (2)
    M 203:4 AnalysisController._batch_generate_descriptions - A (2)
    M 272:4 AnalysisController._on_analysis_start - A (2)
    M 277:4 AnalysisController._on_analysis_progress - A (2)
    M 35:4 AnalysisController.__init__ - A (1)
    M 60:4 AnalysisController.setup_callbacks - A (1)
    M 70:4 AnalysisController.analyze_single - A (1)
    M 121:4 AnalysisController.stop_analysis - A (1)
    M 297:4 AnalysisController._on_analysis_error - A (1)
ui\controllers\collection_controller.py
    M 41:4 CollectionController.remove_project - A (5)
    C 11:0 CollectionController - A (4)
    M 28:4 CollectionController.add_project - A (4)
    M 57:4 CollectionController.create_collection_with_project - A (4)
    M 21:4 CollectionController.__init__ - A (1)
ui\controllers\optimized_display_controller.py
    M 117:4 BaseDisplayController.get_filtered_projects - E (39)
    M 173:4 BaseDisplayController.apply_sorting - B (10)
    C 23:0 BaseDisplayController - A (4)
    C 248:0 OptimizedDisplayController - A (4)
    M 251:4 OptimizedDisplayController.__init__ - A (4)
    M 281:4 OptimizedDisplayController.get_filtered_projects - A (3)
    M 301:4 OptimizedDisplayController._get_page_items - A (3)
    M 57:4 BaseDisplayController.add_filter_chip - A (2)
    M 64:4 BaseDisplayController.remove_filter_chip - A (2)
    M 89:4 BaseDisplayController.set_category_filter - A (2)
    M 198:4 BaseDisplayController.next_page - A (2)
    M 203:4 BaseDisplayController.prev_page - A (2)
    M 231:4 BaseDisplayController._trigger_update - A (2)
    M 235:4 BaseDisplayController.get_display_state - A (2)
    M 297:4 OptimizedDisplayController.invalidate_cache - A (2)
    M 26:4 BaseDisplayController.__init__ - A (1)
    M 47:4 BaseDisplayController.set_filter - A (1)
    M 70:4 BaseDisplayController.clear_all_filters - A (1)
    M 75:4 BaseDisplayController.set_search_query - A (1)
    M 80:4 BaseDisplayController.set_origin_filter - A (1)
    M 99:4 BaseDisplayController.set_tag_filter - A (1)
    M 108:4 BaseDisplayController.set_collection_filter - A (1)
    M 168:4 BaseDisplayController.set_sorting - A (1)
    M 208:4 BaseDisplayController.first_page - A (1)
    M 212:4 BaseDisplayController.last_page - A (1)
    M 216:4 BaseDisplayController.get_page_info - A (1)
ui\controllers\selection_controller.py
    M 102:4 SelectionController.remove_selected - B (10)
    C 17:0 SelectionController - B (6)
    M 55:4 SelectionController.toggle_project - A (5)
    M 75:4 SelectionController.select_all - A (5)
    M 43:4 SelectionController.toggle_mode - A (4)
    M 90:4 SelectionController.deselect_all - A (4)
    M 27:4 SelectionController.__init__ - A (1)
ui\factories\card_factory.py
    M 34:4 CardFactory.create_card - C (12)
    C 11:0 CardFactory - B (6)
    M 71:4 CardFactory.create_batch - A (3)
    M 21:4 CardFactory.__init__ - A (1)
ui\managers\collection_dialog_manager.py
    M 28:4 CollectionDialogManager.new_collection_with - A (4)
    C 7:0 CollectionDialogManager - A (3)
    M 16:4 CollectionDialogManager.add_to_collection - A (2)
    M 22:4 CollectionDialogManager.remove_from_collection - A (2)
    M 38:4 CollectionDialogManager.open_collections_dialog - A (2)
    M 8:4 CollectionDialogManager.__init__ - A (1)
ui\managers\dialog_manager.py
    M 28:4 DialogManager.open_categories_picker - B (7)
    C 24:0 DialogManager - A (3)
    M 107:4 DialogManager.export_database - A (2)
    M 128:4 DialogManager.import_database - A (2)
    M 156:4 DialogManager.manual_backup - A (1)
    M 167:4 DialogManager.open_prepare_folders - A (1)
    M 177:4 DialogManager.open_model_settings - A (1)
ui\managers\modal_generator.py
    C 16:0 ModalGenerator - A (2)
    M 19:4 ModalGenerator.__init__ - A (1)
    M 30:4 ModalGenerator.generate_description - A (1)
ui\managers\modal_manager.py
    M 82:4 ModalManager._handle_close - A (3)
    C 17:0 ModalManager - A (2)
    M 35:4 ModalManager.open_collections - A (2)
    M 44:4 ModalManager.open_prepare_folders - A (2)
    M 50:4 ModalManager.open_import - A (2)
    M 56:4 ModalManager.open_model_settings - A (2)
    M 27:4 ModalManager.__init__ - A (1)
    M 62:4 ModalManager.confirm - A (1)
    M 66:4 ModalManager.info - A (1)
    M 70:4 ModalManager.error - A (1)
    M 74:4 ModalManager.warning - A (1)
    M 78:4 ModalManager.ask_string - A (1)
ui\managers\orphan_manager.py
    M 32:4 OrphanManager.clean_orphans - B (9)
    C 15:0 OrphanManager - B (6)
    M 18:4 OrphanManager.__init__ - A (1)
ui\managers\progress_ui_manager.py
    C 5:0 ProgressUIManager - A (2)
    M 21:4 ProgressUIManager.update - A (2)
    M 6:4 ProgressUIManager.__init__ - A (1)
    M 12:4 ProgressUIManager.show - A (1)
    M 17:4 ProgressUIManager.hide - A (1)
ui\managers\toggle_manager.py
    M 19:4 ToggleManager._toggle_field - B (7)
    C 13:0 ToggleManager - A (3)
    M 14:4 ToggleManager.__init__ - A (1)
    M 54:4 ToggleManager.toggle_favorite - A (1)
    M 64:4 ToggleManager.toggle_done - A (1)
    M 74:4 ToggleManager.toggle_good - A (1)
    M 81:4 ToggleManager.toggle_bad - A (1)
utils\duplicate_detector.py
    M 106:4 DuplicateDetector.find_duplicates - A (5)
    M 192:4 DuplicateDetector.get_duplicate_summary - A (4)
    C 45:0 DuplicateDetector - A (3)
    M 58:4 DuplicateDetector.__init__ - A (1)
    M 61:4 DuplicateDetector.normalize_folder_name - A (1)
    M 155:4 DuplicateDetector.is_duplicate - A (1)
utils\logging_setup.py
    F 9:0 setup_logging - A (2)
utils\name_translator.py
    F 410:0 search_bilingual - B (6)
    F 348:0 translate_to_pt - A (4)
    F 379:0 translate_to_en - A (4)
utils\platform_utils.py
    F 10:0 open_folder - A (5)
    F 30:0 open_file - A (5)
utils\recursive_scanner.py
    M 106:4 RecursiveScanner._scan_recursive - C (13)
    C 32:0 RecursiveScanner - A (4)
    M 164:4 RecursiveScanner._has_project_files - A (3)
    M 53:4 RecursiveScanner.scan_folders_pure - A (2)
    M 67:4 RecursiveScanner.scan_folders_hybrid - A (2)
    M 83:4 RecursiveScanner.generate_unique_id - A (2)
    M 41:4 RecursiveScanner.__init__ - A (1)
    M 92:4 RecursiveScanner.get_stats - A (1)
    M 95:4 RecursiveScanner._reset_stats - A (1)
    M 161:4 RecursiveScanner._is_technical_subfolder - A (1)
utils\text_utils.py
    F 9:0 remove_accents - A (3)
    F 29:0 normalize_project_name - A (2)

498 blocks (classes, functions, methods) analyzed.
Average complexity: A (3.110441767068273)

```

## 04_radon_raw.txt
```text
main.py
    LOC: 27
    LLOC: 18
    SLOC: 17
    Comments: 0
    Single comments: 0
    Multi: 4
    Blank: 6
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 15%
ai\analysis_manager.py
    LOC: 293
    LLOC: 162
    SLOC: 160
    Comments: 23
    Single comments: 18
    Multi: 51
    Blank: 64
    - Comment Stats
        (C % L): 8%
        (C % S): 14%
        (C + M % L): 25%
ai\fallbacks.py
    LOC: 553
    LLOC: 211
    SLOC: 355
    Comments: 66
    Single comments: 58
    Multi: 67
    Blank: 73
    - Comment Stats
        (C % L): 12%
        (C % S): 19%
        (C + M % L): 24%
ai\image_analyzer.py
    LOC: 131
    LLOC: 50
    SLOC: 71
    Comments: 9
    Single comments: 9
    Multi: 30
    Blank: 21
    - Comment Stats
        (C % L): 7%
        (C % S): 13%
        (C + M % L): 30%
ai\keyword_maps.py
    LOC: 855
    LLOC: 14
    SLOC: 689
    Comments: 145
    Single comments: 36
    Multi: 13
    Blank: 117
    - Comment Stats
        (C % L): 17%
        (C % S): 21%
        (C + M % L): 18%
ai\ollama_client.py
    LOC: 220
    LLOC: 106
    SLOC: 160
    Comments: 10
    Single comments: 8
    Multi: 23
    Blank: 29
    - Comment Stats
        (C % L): 5%
        (C % S): 6%
        (C + M % L): 15%
ai\text_generator.py
    LOC: 411
    LLOC: 128
    SLOC: 240
    Comments: 46
    Single comments: 35
    Multi: 66
    Blank: 70
    - Comment Stats
        (C % L): 11%
        (C % S): 19%
        (C + M % L): 27%
ai\__init__.py
    LOC: 1
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
config\card_layout.py
    LOC: 28
    LLOC: 6
    SLOC: 5
    Comments: 8
    Single comments: 3
    Multi: 15
    Blank: 5
    - Comment Stats
        (C % L): 29%
        (C % S): 160%
        (C + M % L): 82%
config\constants.py
    LOC: 101
    LLOC: 9
    SLOC: 65
    Comments: 41
    Single comments: 12
    Multi: 14
    Blank: 10
    - Comment Stats
        (C % L): 41%
        (C % S): 63%
        (C + M % L): 54%
config\settings.py
    LOC: 80
    LLOC: 26
    SLOC: 36
    Comments: 37
    Single comments: 30
    Multi: 3
    Blank: 11
    - Comment Stats
        (C % L): 46%
        (C % S): 103%
        (C + M % L): 50%
config\ui_constants.py
    LOC: 151
    LLOC: 57
    SLOC: 73
    Comments: 81
    Single comments: 44
    Multi: 4
    Blank: 30
    - Comment Stats
        (C % L): 54%
        (C % S): 111%
        (C + M % L): 56%
config\__init__.py
    LOC: 1
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
core\collections_manager.py
    LOC: 290
    LLOC: 148
    SLOC: 160
    Comments: 3
    Single comments: 11
    Multi: 61
    Blank: 58
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 22%
core\database.py
    LOC: 284
    LLOC: 178
    SLOC: 186
    Comments: 4
    Single comments: 18
    Multi: 27
    Blank: 53
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 11%
core\database_controller.py
    LOC: 123
    LLOC: 57
    SLOC: 85
    Comments: 3
    Single comments: 6
    Multi: 12
    Blank: 20
    - Comment Stats
        (C % L): 2%
        (C % S): 4%
        (C + M % L): 12%
core\project_scanner.py
    LOC: 190
    LLOC: 101
    SLOC: 120
    Comments: 14
    Single comments: 14
    Multi: 21
    Blank: 35
    - Comment Stats
        (C % L): 7%
        (C % S): 12%
        (C + M % L): 18%
core\protocols.py
    LOC: 46
    LLOC: 28
    SLOC: 17
    Comments: 0
    Single comments: 5
    Multi: 11
    Blank: 13
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 24%
core\thumbnail_cache.py
    LOC: 263
    LLOC: 156
    SLOC: 150
    Comments: 14
    Single comments: 10
    Multi: 70
    Blank: 33
    - Comment Stats
        (C % L): 5%
        (C % S): 9%
        (C + M % L): 32%
core\thumbnail_preloader.py
    LOC: 331
    LLOC: 126
    SLOC: 141
    Comments: 20
    Single comments: 17
    Multi: 114
    Blank: 59
    - Comment Stats
        (C % L): 6%
        (C % S): 14%
        (C + M % L): 40%
core\virtual_scroll_manager.py
    LOC: 305
    LLOC: 121
    SLOC: 133
    Comments: 36
    Single comments: 28
    Multi: 85
    Blank: 59
    - Comment Stats
        (C % L): 12%
        (C % S): 27%
        (C + M % L): 40%
core\__init__.py
    LOC: 1
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
core\performance\filter_cache.py
    LOC: 203
    LLOC: 72
    SLOC: 90
    Comments: 13
    Single comments: 11
    Multi: 67
    Blank: 35
    - Comment Stats
        (C % L): 6%
        (C % S): 14%
        (C + M % L): 39%
core\performance\predictive_preloader.py
    LOC: 216
    LLOC: 74
    SLOC: 100
    Comments: 18
    Single comments: 11
    Multi: 70
    Blank: 35
    - Comment Stats
        (C % L): 8%
        (C % S): 18%
        (C + M % L): 41%
core\performance\viewport_manager.py
    LOC: 217
    LLOC: 76
    SLOC: 100
    Comments: 17
    Single comments: 11
    Multi: 70
    Blank: 36
    - Comment Stats
        (C % L): 8%
        (C % S): 17%
        (C + M % L): 40%
core\performance\__init__.py
    LOC: 21
    LLOC: 5
    SLOC: 8
    Comments: 0
    Single comments: 0
    Multi: 9
    Blank: 4
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 43%
ui\collections_dialog.py
    LOC: 389
    LLOC: 183
    SLOC: 271
    Comments: 25
    Single comments: 32
    Multi: 18
    Blank: 68
    - Comment Stats
        (C % L): 6%
        (C % S): 9%
        (C + M % L): 11%
ui\duplicate_resolution_dialog.py
    LOC: 163
    LLOC: 98
    SLOC: 127
    Comments: 4
    Single comments: 4
    Multi: 5
    Blank: 27
    - Comment Stats
        (C % L): 2%
        (C % S): 3%
        (C + M % L): 6%
ui\edit_modal.py
    LOC: 125
    LLOC: 67
    SLOC: 96
    Comments: 4
    Single comments: 4
    Multi: 10
    Blank: 15
    - Comment Stats
        (C % L): 3%
        (C % S): 4%
        (C + M % L): 11%
ui\header.py
    LOC: 308
    LLOC: 93
    SLOC: 197
    Comments: 58
    Single comments: 41
    Multi: 40
    Blank: 30
    - Comment Stats
        (C % L): 19%
        (C % S): 29%
        (C + M % L): 32%
ui\import_mode_dialog.py
    LOC: 198
    LLOC: 108
    SLOC: 150
    Comments: 10
    Single comments: 10
    Multi: 9
    Blank: 29
    - Comment Stats
        (C % L): 5%
        (C % S): 7%
        (C + M % L): 10%
ui\import_preview_dialog.py
    LOC: 133
    LLOC: 79
    SLOC: 103
    Comments: 3
    Single comments: 3
    Multi: 5
    Blank: 22
    - Comment Stats
        (C % L): 2%
        (C % S): 3%
        (C + M % L): 6%
ui\main_window.py
    LOC: 581
    LLOC: 329
    SLOC: 415
    Comments: 38
    Single comments: 40
    Multi: 32
    Blank: 94
    - Comment Stats
        (C % L): 7%
        (C % S): 9%
        (C + M % L): 12%
ui\model_settings_dialog.py
    LOC: 298
    LLOC: 146
    SLOC: 224
    Comments: 17
    Single comments: 16
    Multi: 17
    Blank: 41
    - Comment Stats
        (C % L): 6%
        (C % S): 8%
        (C + M % L): 11%
ui\prepare_folders_dialog.py
    LOC: 212
    LLOC: 133
    SLOC: 172
    Comments: 5
    Single comments: 5
    Multi: 5
    Blank: 30
    - Comment Stats
        (C % L): 2%
        (C % S): 3%
        (C + M % L): 5%
ui\project_card.py
    LOC: 397
    LLOC: 194
    SLOC: 257
    Comments: 31
    Single comments: 27
    Multi: 48
    Blank: 65
    - Comment Stats
        (C % L): 8%
        (C % S): 12%
        (C + M % L): 20%
ui\project_modal.py
    LOC: 410
    LLOC: 284
    SLOC: 327
    Comments: 16
    Single comments: 16
    Multi: 21
    Blank: 46
    - Comment Stats
        (C % L): 4%
        (C % S): 5%
        (C + M % L): 9%
ui\recursive_import_integration.py
    LOC: 470
    LLOC: 234
    SLOC: 304
    Comments: 44
    Single comments: 45
    Multi: 57
    Blank: 64
    - Comment Stats
        (C % L): 9%
        (C % S): 14%
        (C + M % L): 21%
ui\sidebar.py
    LOC: 273
    LLOC: 160
    SLOC: 204
    Comments: 20
    Single comments: 16
    Multi: 27
    Blank: 26
    - Comment Stats
        (C % L): 7%
        (C % S): 10%
        (C + M % L): 17%
ui\virtual_scroll.py
    LOC: 249
    LLOC: 117
    SLOC: 109
    Comments: 41
    Single comments: 25
    Multi: 63
    Blank: 52
    - Comment Stats
        (C % L): 16%
        (C % S): 38%
        (C + M % L): 42%
ui\__init__.py
    LOC: 1
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
ui\builders\cards_grid_builder.py
    LOC: 51
    LLOC: 16
    SLOC: 20
    Comments: 0
    Single comments: 1
    Multi: 22
    Blank: 8
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 43%
ui\builders\header_builder.py
    LOC: 133
    LLOC: 44
    SLOC: 56
    Comments: 7
    Single comments: 8
    Multi: 44
    Blank: 25
    - Comment Stats
        (C % L): 5%
        (C % S): 12%
        (C + M % L): 38%
ui\builders\navigation_builder.py
    LOC: 202
    LLOC: 48
    SLOC: 130
    Comments: 14
    Single comments: 15
    Multi: 31
    Blank: 26
    - Comment Stats
        (C % L): 7%
        (C % S): 11%
        (C + M % L): 22%
ui\builders\ui_builder.py
    LOC: 156
    LLOC: 75
    SLOC: 103
    Comments: 8
    Single comments: 13
    Multi: 16
    Blank: 24
    - Comment Stats
        (C % L): 5%
        (C % S): 8%
        (C + M % L): 15%
ui\components\chips_bar.py
    LOC: 184
    LLOC: 87
    SLOC: 105
    Comments: 16
    Single comments: 20
    Multi: 26
    Blank: 33
    - Comment Stats
        (C % L): 9%
        (C % S): 15%
        (C + M % L): 23%
ui\components\pagination_controls.py
    LOC: 10
    LLOC: 3
    SLOC: 2
    Comments: 0
    Single comments: 0
    Multi: 6
    Blank: 2
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 60%
ui\components\selection_bar.py
    LOC: 160
    LLOC: 65
    SLOC: 107
    Comments: 12
    Single comments: 17
    Multi: 11
    Blank: 25
    - Comment Stats
        (C % L): 8%
        (C % S): 11%
        (C + M % L): 14%
ui\components\status_bar.py
    LOC: 70
    LLOC: 34
    SLOC: 41
    Comments: 3
    Single comments: 7
    Multi: 11
    Blank: 11
    - Comment Stats
        (C % L): 4%
        (C % S): 7%
        (C + M % L): 20%
ui\components\__init__.py
    LOC: 8
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 0
    Multi: 6
    Blank: 2
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 75%
ui\controllers\analysis_controller.py
    LOC: 299
    LLOC: 143
    SLOC: 143
    Comments: 20
    Single comments: 23
    Multi: 75
    Blank: 58
    - Comment Stats
        (C % L): 7%
        (C % S): 14%
        (C + M % L): 32%
ui\controllers\collection_controller.py
    LOC: 75
    LLOC: 38
    SLOC: 36
    Comments: 7
    Single comments: 9
    Multi: 12
    Blank: 18
    - Comment Stats
        (C % L): 9%
        (C % S): 19%
        (C + M % L): 25%
ui\controllers\optimized_display_controller.py
    LOC: 306
    LLOC: 226
    SLOC: 246
    Comments: 4
    Single comments: 6
    Multi: 9
    Blank: 45
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 4%
ui\controllers\selection_controller.py
    LOC: 143
    LLOC: 83
    SLOC: 85
    Comments: 12
    Single comments: 12
    Multi: 15
    Blank: 31
    - Comment Stats
        (C % L): 8%
        (C % S): 14%
        (C + M % L): 19%
ui\controllers\__init__.py
    LOC: 8
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 0
    Multi: 6
    Blank: 2
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 75%
ui\factories\card_factory.py
    LOC: 92
    LLOC: 52
    SLOC: 42
    Comments: 3
    Single comments: 3
    Multi: 31
    Blank: 16
    - Comment Stats
        (C % L): 3%
        (C % S): 7%
        (C + M % L): 37%
ui\managers\collection_dialog_manager.py
    LOC: 48
    LLOC: 35
    SLOC: 40
    Comments: 1
    Single comments: 2
    Multi: 0
    Blank: 6
    - Comment Stats
        (C % L): 2%
        (C % S): 2%
        (C + M % L): 2%
ui\managers\dialog_manager.py
    LOC: 184
    LLOC: 86
    SLOC: 106
    Comments: 0
    Single comments: 1
    Multi: 47
    Blank: 30
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 26%
ui\managers\modal_generator.py
    LOC: 83
    LLOC: 31
    SLOC: 46
    Comments: 6
    Single comments: 7
    Multi: 17
    Blank: 13
    - Comment Stats
        (C % L): 7%
        (C % S): 13%
        (C + M % L): 28%
ui\managers\modal_manager.py
    LOC: 88
    LLOC: 59
    SLOC: 47
    Comments: 1
    Single comments: 11
    Multi: 13
    Blank: 17
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 16%
ui\managers\orphan_manager.py
    LOC: 78
    LLOC: 35
    SLOC: 50
    Comments: 6
    Single comments: 8
    Multi: 8
    Blank: 12
    - Comment Stats
        (C % L): 8%
        (C % S): 12%
        (C + M % L): 18%
ui\managers\progress_ui_manager.py
    LOC: 25
    LLOC: 20
    SLOC: 18
    Comments: 1
    Single comments: 2
    Multi: 0
    Blank: 5
    - Comment Stats
        (C % L): 4%
        (C % S): 6%
        (C + M % L): 4%
ui\managers\toggle_manager.py
    LOC: 86
    LLOC: 40
    SLOC: 40
    Comments: 8
    Single comments: 12
    Multi: 16
    Blank: 18
    - Comment Stats
        (C % L): 9%
        (C % S): 20%
        (C + M % L): 28%
utils\duplicate_detector.py
    LOC: 274
    LLOC: 63
    SLOC: 81
    Comments: 19
    Single comments: 19
    Multi: 116
    Blank: 58
    - Comment Stats
        (C % L): 7%
        (C % S): 23%
        (C + M % L): 49%
utils\logging_setup.py
    LOC: 47
    LLOC: 19
    SLOC: 24
    Comments: 5
    Single comments: 5
    Multi: 7
    Blank: 11
    - Comment Stats
        (C % L): 11%
        (C % S): 21%
        (C + M % L): 26%
utils\name_translator.py
    LOC: 449
    LLOC: 46
    SLOC: 360
    Comments: 25
    Single comments: 11
    Multi: 36
    Blank: 42
    - Comment Stats
        (C % L): 6%
        (C % S): 7%
        (C + M % L): 14%
utils\platform_utils.py
    LOC: 47
    LLOC: 35
    SLOC: 32
    Comments: 4
    Single comments: 0
    Multi: 9
    Blank: 6
    - Comment Stats
        (C % L): 9%
        (C % S): 12%
        (C + M % L): 28%
utils\recursive_scanner.py
    LOC: 169
    LLOC: 99
    SLOC: 127
    Comments: 2
    Single comments: 2
    Multi: 15
    Blank: 25
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 10%
utils\text_utils.py
    LOC: 69
    LLOC: 16
    SLOC: 16
    Comments: 5
    Single comments: 5
    Multi: 31
    Blank: 17
    - Comment Stats
        (C % L): 7%
        (C % S): 31%
        (C + M % L): 52%
utils\__init__.py
    LOC: 1
    LLOC: 1
    SLOC: 0
    Comments: 0
    Single comments: 1
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%

```

## 05_vulture.txt
```text
core\protocols.py:46: unused variable 'project_count' (100% confidence)
core\thumbnail_preloader.py:26: unused import 'as_completed' (90% confidence)
ui\components\chips_bar.py:10: unused import 'ACCENT_BLUE' (90% confidence)
ui\project_modal.py:353: unused variable 'ev' (100% confidence)

```

## 06_duplication.txt
```text
Nenhuma duplica��o literal relevante encontrada.

```

## 07_unit_pytest.txt
```text
F....                                                                    [100%]
================================== FAILURES ===================================
____________________ test_no_pyc_committed_in_source_tree _____________________

    def test_no_pyc_committed_in_source_tree() -> None:
        offenders = [str(p) for p in Path(".").rglob("*.pyc") if ".venv" not in str(p)]
>       assert not offenders, "Arquivos .pyc presentes na arvore: " + ", ".join(offenders[:50])
E       AssertionError: Arquivos .pyc presentes na arvore: __pycache__\main.cpython-314.pyc, utils\__pycache__\duplicate_detector.cpython-314.pyc, utils\__pycache__\logging_setup.cpython-314.pyc, utils\__pycache__\name_translator.cpython-314.pyc, utils\__pycache__\platform_utils.cpython-314.pyc, utils\__pycache__\recursive_scanner.cpython-314.pyc, utils\__pycache__\text_utils.cpython-314.pyc, utils\__pycache__\__init__.cpython-314.pyc, ui\__pycache__\collections_dialog.cpython-314.pyc, ui\__pycache__\duplicate_resolution_dialog.cpython-314.pyc, ui\__pycache__\edit_modal.cpython-314.pyc, ui\__pycache__\header.cpython-314.pyc, ui\__pycache__\import_mode_dialog.cpython-314.pyc, ui\__pycache__\import_preview_dialog.cpython-314.pyc, ui\__pycache__\main_window.cpython-314.pyc, ui\__pycache__\model_settings_dialog.cpython-314.pyc, ui\__pycache__\prepare_folders_dialog.cpython-314.pyc, ui\__pycache__\project_card.cpython-314.pyc, ui\__pycache__\project_modal.cpython-314.pyc, ui\__pycache__\recursive_import_integration.cpython-314.pyc, ui\__pycache__\sidebar.cpython-314.pyc, ui\__pycache__\virtual_scroll.cpython-314.pyc, ui\__pycache__\__init__.cpython-314.pyc, ui\managers\__pycache__\collection_dialog_manager.cpython-314.pyc, ui\managers\__pycache__\dialog_manager.cpython-314.pyc, ui\managers\__pycache__\modal_generator.cpython-314.pyc, ui\managers\__pycache__\modal_manager.cpython-314.pyc, ui\managers\__pycache__\orphan_manager.cpython-314.pyc, ui\managers\__pycache__\progress_ui_manager.cpython-314.pyc, ui\managers\__pycache__\toggle_manager.cpython-314.pyc, ui\factories\__pycache__\card_factory.cpython-314.pyc, ui\controllers\__pycache__\analysis_controller.cpython-314.pyc, ui\controllers\__pycache__\collection_controller.cpython-314.pyc, ui\controllers\__pycache__\optimized_display_controller.cpython-314.pyc, ui\controllers\__pycache__\selection_controller.cpython-314.pyc, ui\controllers\__pycache__\__init__.cpython-314.pyc, ui\components\__pycache__\chips_bar.cpython-314.pyc, ui\components\__pycache__\pagination_controls.cpython-314.pyc, ui\components\__pycache__\selection_bar.cpython-314.pyc, ui\components\__pycache__\status_bar.cpython-314.pyc, ui\components\__pycache__\__init__.cpython-314.pyc, ui\builders\__pycache__\cards_grid_builder.cpython-314.pyc, ui\builders\__pycache__\header_builder.cpython-314.pyc, ui\builders\__pycache__\navigation_builder.cpython-314.pyc, ui\builders\__pycache__\ui_builder.cpython-314.pyc, tests\__pycache__\conftest.cpython-314-pytest-9.0.2.pyc, tests\unit\__pycache__\test_no_runtime_artifacts_committed.cpython-314-pytest-9.0.2.pyc, tests\unit\__pycache__\test_project_structure.cpython-314-pytest-9.0.2.pyc, tests\unit\__pycache__\test_python_files_compile.cpython-314-pytest-9.0.2.pyc, core\__pycache__\collections_manager.cpython-314.pyc
E       assert not ['__pycache__\\main.cpython-314.pyc', 'utils\\__pycache__\\duplicate_detector.cpython-314.pyc', 'utils\\__pycache__\\l...c', 'utils\\__pycache__\\platform_utils.cpython-314.pyc', 'utils\\__pycache__\\recursive_scanner.cpython-314.pyc', ...]

tests\unit\test_no_runtime_artifacts_committed.py:5: AssertionError
=========================== short test summary info ===========================
FAILED tests/unit/test_no_runtime_artifacts_committed.py::test_no_pyc_committed_in_source_tree
1 failed, 4 passed in 0.85s

```

## 08_integration_pytest.txt
```text
...                                                                      [100%]
3 passed in 0.18s

```

## 09_smoke_pytest.txt
```text
.                                                                        [100%]
1 passed in 0.38s

```

## Nova pasta
```text
[ERRO AO LER QA\reports\Nova pasta: [Errno 13] Permission denied: 'QA\\reports\\Nova pasta']
```
