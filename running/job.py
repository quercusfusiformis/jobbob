from typing import List

class Job:
    def __init__(self,
                    inputfilename: str,
                    nprocshared: int,
                    mem: str,
                    nodes: int=1,
                    verbosity: str="verbose",
                    export: str="ALL",
                    time: str="72:00:00",
                    qos: str="normal",
                    mail_type: str="NONE",
                    mail_user: str="NONE@pm.me",
                    partition: List[str] = ["msg","bus","physics","pws","m9pws","pws3","mkt24","m11-1",
                                            "m11-2","m8","m8n","m9","m8g","m9g","paulbryf","bio","bep8"]):
        partitionstring: str = ",".join(partition)
        self.contents: str = (
                            f"#!/bin/bash\n"
                            f"#SBATCH --{verbosity}\n"
                            f"#SBATCH --nodes={nodes}\n"
                            f"#SBATCH --ntasks-per-node={nprocshared}\n"
                            f"#SBATCH --mem={mem}\n"
                            f"#SBATCH --export={export}\n"
                            f"#SBATCH --qos={qos}\n"
                            f"#SBATCH --mail-type={mail_type}\n"
                            f"#SBATCH --mail-user={mail_user}\n"
                            f"#SBATCH --partition={partitionstring}\n"
                            "\nmodule load g16\n"
                            "#cd \$SBATCH_O_WORKDIR\n"
                            "[ \`cat /proc/cpuinfo | grep -m 1 vendor_id | awk '{print \$3}'\` == 'AuthenticAMD' ] && export PGI_FASTMATH_CPU=haswell\n"
                            "export GAUSS_SCRDIR=/tmp/\${SLURM_JOB_ID}\n"
                            "mkdir -p \$GAUSS_SCRDIR\n"
                            f"g16 {inputfilename}\n\n"
                            )
    
    def get_contents(self) -> str:
        return self.contents


if __name__ == "__main__":
    job = Job("file.com", 16, "32GB", qos="standby")
    print(job.get_contents())
