import sys, os

sys.path[0] += "/.."
os.chdir("..")

import services.processing_worker as processing_worker


if __name__ == "__main__":
    processing_task_id = None

    def set_processing_task_id(id):
        global processing_task_id
        processing_task_id = id

    try:
        processing_worker.connect(set_processing_task_id)
    except KeyboardInterrupt:
        print("Interrupted")
        processing_worker.handle_exit(processing_task_id)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as e:
        print(f"Crashed on process ID={processing_task_id}:", e)
        processing_worker.handle_exit(processing_task_id)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
