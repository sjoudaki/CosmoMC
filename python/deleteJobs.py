from __future__ import absolute_import
from __future__ import print_function
import subprocess

from paramgrid import batchjob_args, jobqueue
from six.moves import range


Opts = batchjob_args.batchArgs('Delete running or queued jobs', importance=True, batchPathOptional=True)

group = Opts.parser.add_mutually_exclusive_group()
group.add_argument('--queued', action='store_true')
group.add_argument('--running', action='store_true')

Opts.parser.add_argument('--delete_id_min', type=int)
Opts.parser.add_argument('--delete_id_range', nargs=2, type=int)
Opts.parser.add_argument('--delete_ids', nargs='+', type=int)

Opts.parser.add_argument('--confirm', action='store_true')


(batch, args) = Opts.parseForBatch()


if batch:
    if args.delete_id_range is not None:
        jobqueue.deleteJobs(args.batchPath, jobId_minmax=args.delete_id_range, confirm=args.confirm)
    if args.delete_id_min is not None:
        jobqueue.deleteJobs(args.batchPath, jobId_min=args.delete_id_min, confirm=args.confirm)
    elif args.delete_ids is not None:
        jobqueue.deleteJobs(args.batchPath, args.delete_ids, confirm=args.confirm)
    else:
        items = [jobItem for jobItem in Opts.filteredBatchItems()]
        batchNames = set([jobItem.name for jobItem in items])
        jobqueue.deleteJobs(args.batchPath, rootNames=batchNames, confirm=args.confirm)

    if not args.confirm: print('jobs not actually deleted: add --confirm to really cancel them')

else:
    ids = []
    if args.delete_id_range is not None: ids = list(range(args.delete_id_range[0], args.delete_id_range[1] + 1))
    elif args.delete_ids is not None: ids += args.delete_ids
    else: print('Must give --delete_id_range or --delete_ids if no batch directory')
    for jobId in ids:
        subprocess.check_output('qdel ' + str(jobId), shell=True).strip()
