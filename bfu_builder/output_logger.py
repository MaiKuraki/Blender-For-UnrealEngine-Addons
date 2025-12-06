import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class BuilderLogger:
    """Simple logger that captures all output to a temporary file"""
    def __init__(self):
        self.log_file_path: Optional[Path] = None
        self.log_file = None
        self.original_stdout = None
        self.original_stderr = None
    
    def start(self):
        """Start capturing output to log file"""
        # Create temp log file
        import tempfile
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = Path(tempfile.gettempdir())
        self.log_file_path = temp_dir / f"bfu_builder_{timestamp}.log"
        
        # Open log file
        self.log_file = open(self.log_file_path, 'w', encoding='utf-8')
        
        # Redirect stdout and stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self._TeeOutput(sys.stdout, self.log_file)
        sys.stderr = self._TeeOutput(sys.stderr, self.log_file)
    
    def stop(self):
        """Stop capturing and restore original output"""
        if self.original_stdout:
            sys.stdout = self.original_stdout
        if self.original_stderr:
            sys.stderr = self.original_stderr
        if self.log_file:
            self.log_file.close()
    
    def get_log_path(self) -> Optional[str]:
        """Get the path to the log file"""
        return str(self.log_file_path) if self.log_file_path else None
    
    class _TeeOutput:
        """Internal class to write to both console and file"""
        def __init__(self, terminal, log_file):
            self.terminal = terminal
            self.log_file = log_file
        
        def write(self, message):
            self.terminal.write(message)
            self.log_file.write(message)
            self.log_file.flush()
        
        def flush(self):
            self.terminal.flush()
            self.log_file.flush()
