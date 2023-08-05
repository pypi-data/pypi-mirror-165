__scriptname__ = 'exoclasma-index'
__version__ = '0.9.5'
__bugtracker__ = 'https://github.com/regnveig/exoclasma-index/issues'

from Bio import SeqIO #
import argparse
import bz2
import datetime
import gzip
import json
import logging
import os
import pandas #
import re
import subprocess
import sys
import tempfile

# -----=====| LOGGING |=====-----

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

# -----=====| DEPS |=====-----

def CheckDependency(Name):
	Shell = subprocess.Popen(Name, shell = True, executable = 'bash', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	Stdout, _ = Shell.communicate()
	if Shell.returncode == 127:
		logging.error(f'Dependency "{Name}" is not found!')
		exit(1)
	if Shell.returncode == 126:
		logging.error(f'Dependency "{Name}" is not executable!')
		exit(1)

def CheckDependencies(CheckGatk = True):
	CheckDependency('samtools')
	CheckDependency('bwa')
	CheckDependency('bedtools')
	if CheckGatk: CheckDependency('gatk')


## ------======| MISC |======------

def Open(FileName):
	GzipCheck = lambda FileName: open(FileName, 'rb').read(2).hex() == '1f8b'
	Bzip2Check = lambda FileName: open(FileName, 'rb').read(3).hex() == '425a68'
	CheckFlags = GzipCheck(FileName = FileName), Bzip2Check(FileName = FileName)
	OpenFunc = { (0, 1): bz2.open, (1, 0): gzip.open, (0, 0): open }[CheckFlags]
	return OpenFunc(FileName, 'rt')

def ArmorDoubleQuotes(String): return f'"{String}"'

def ArmorSingleQuotes(String): return f"'{String}'"

def BashSubprocess(SuccessMessage, Command):
	logging.debug(f'Shell command: {Command}')
	Shell = subprocess.Popen(Command, shell = True, executable = 'bash', stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	_, Stderr = Shell.communicate()
	if (Shell.returncode != 0):
		logging.error(f'Shell command returned non-zero exit code {Shell.returncode}: {Command}\n{Stderr.decode("utf-8")}')
		exit(1)
	logging.info(SuccessMessage)

## ------======| REFSEQ PREP |======------

def CreateGenomeInfo(GenomeName, RestrictionEnzymes, Description = None, BuildGatkIndex = True):
	ConfigJson = {
		'name':               str(GenomeName),
		'description':        Description,
		'created':            datetime.datetime.now().isoformat(),
		'fasta':              f'{GenomeName}.fa',
		'chrom.sizes':        f'{GenomeName}.chrom.sizes',
		'samtools.faidx':     f'{GenomeName}.fa.fai',
		'bed':                f'{GenomeName}.bed',
		'gatk.dict':          f'{GenomeName}.dict' if BuildGatkIndex else None,
		'juicer.rs':          { Name: { 'map': os.path.join('juicer.rs', f'{GenomeName}.rs.{Name}.txt'), 'site': str(Site) } for Name, Site in RestrictionEnzymes.items() },
		'capture':            dict()
	}
	return ConfigJson

def RefseqPreparation(GenomeName, FastaPath, ParentDir, Description, BuildGatkIndex, ContigJSON):
	logging.info(f'{__scriptname__} Reference {__version__}')
	# Config
	ConfigPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	Config = json.load(open(ConfigPath, 'rt'))
	if ContigJSON is not None: ContigList = json.loads(ContigJSON)
	# Output Dir
	OutputDir = os.path.realpath(os.path.join(ParentDir, GenomeName))
	RSDir = os.path.realpath(os.path.join(OutputDir, 'juicer.rs'))
	os.mkdir(OutputDir)
	os.mkdir(RSDir)
	logging.info(f'Directory created: {OutputDir}')
	# Open fasta
	FullFastaPath = os.path.realpath(FastaPath)
	Fasta = SeqIO.parse(Open(FullFastaPath), 'fasta')
	logging.info(f'FASTA opened: {FullFastaPath}')
	SearchQueries = { Name: re.compile(Sequences) for Name, Sequences in Config['Enzymes'].items() }
	GenomeInfo = CreateGenomeInfo(GenomeName, Config['Enzymes'], Description, BuildGatkIndex)
	# Paths
	OutputFasta = os.path.join(OutputDir, GenomeInfo['fasta'])
	ChromSizesPath = os.path.join(OutputDir, GenomeInfo['chrom.sizes'])
	BedPath = os.path.join(OutputDir, GenomeInfo['bed'])
	# Sort & filter
	if ContigJSON is not None:
		if len(set(ContigList)) < len(ContigList):
			logging.error(f'Some contigs from list are duplicated')
			exit(1)
		Contigs = { contig: None for contig in ContigList}
		for Contig in Fasta:
			if Contig.name in Contigs: Contigs[Contig.name] = Contig
		ContigsNotExist = [Item for Item in Contigs if (Contigs[Item] is None)]
		if ContigsNotExist:
			logging.error(f'Some contigs from list not exist: {json.dumps(ContigsNotExist)}')
			exit(1)
	else:
		Contigs = {}
		for Contig in Fasta: Contigs[Contig.name] = Contig
	# TODO Low memory issue
	with open(OutputFasta, 'w') as NewFasta, open(ChromSizesPath, 'w') as ChromSizes, open(BedPath, 'w') as BedFile:
		for Contig in Contigs.values():
			Contig.name = re.sub('[^\w\.]', '_', Contig.name)
			Seq = Contig.seq.__str__()
			ReverseComplementSeq = Contig.seq.reverse_complement().__str__()
			SeqLength = len(Seq)
			SeqIO.write([Contig], NewFasta, 'fasta')
			ChromSizes.write(f'{Contig.name}\t{SeqLength}\n')
			BedFile.write(f'{Contig.name}\t0\t{SeqLength}\n')
			for Enzyme, Query in SearchQueries.items():
				RSPath = os.path.join(OutputDir, GenomeInfo['juicer.rs'][Enzyme]['map'])
				with open(RSPath, 'a') as FileWrapper:
					Sites = [(Match.start() + 1) for Match in Query.finditer(Seq)] + [(SeqLength - Match.end() + 1) for Match in Query.finditer(ReverseComplementSeq)]
					Sites = sorted(list(set(Sites)))
					FileWrapper.write(' '.join([Contig.name] + [str(Item) for Item in Sites] + [str(SeqLength)]) + '\n')
			del Seq
			del ReverseComplementSeq
			logging.info(f'Contig ready: {Contig.name}')
	logging.info('Fasta, chrom sizes, bed file, and restriction sites are ready')
	GenomeInfo['chrom.sizes.dict'] = pandas.read_csv(BedPath, sep = '\t', header = None).set_index(0)[2].to_dict()
	CommandSamtoolsIndex = ['samtools', 'faidx',  ArmorDoubleQuotes(OutputFasta)]
	CommandBwaIndex = ['bwa', 'index',  ArmorDoubleQuotes(OutputFasta)]
	BashSubprocess('SAMtools faidx ready', ' '.join(CommandSamtoolsIndex))
	BashSubprocess('BWA index ready', ' '.join(CommandBwaIndex))
	if BuildGatkIndex:
		CommandGATKIndex = ['gatk', 'CreateSequenceDictionary', '--VERBOSITY', 'ERROR', '-R',  ArmorDoubleQuotes(OutputFasta)]
		BashSubprocess('GATK dictionary ready', ' '.join(CommandGATKIndex))
	GenomeInfoJson = os.path.join(OutputDir, f'{GenomeName}.info.json')
	json.dump(GenomeInfo, open(GenomeInfoJson, 'wt'), indent = 4, ensure_ascii = False)
	logging.info('Job finished')


## ------======| CAPTURE PREP |======------

def CreateCaptureInfo(CaptureName, Description = None):
	ConfigJson = {
		'name':         str(CaptureName),
		'description':  Description,
		'created':      datetime.datetime.now().isoformat(),
		'capture':      os.path.join('capture', CaptureName, f'{CaptureName}.capture.bed'),
		'not.capture':  os.path.join('capture', CaptureName, f'{CaptureName}.not.capture.bed')
	}
	return ConfigJson

def CapturePreparation(CaptureName, InputBED, GenomeInfoJSON, Description):
	logging.info(f'{__scriptname__} Capture {__version__}')
	# Info struct
	GenomeInfoPath = os.path.realpath(GenomeInfoJSON)
	GenomeInfo = json.load(open(GenomeInfoPath, 'rt'))
	logging.info(f'Genome info loaded: {GenomeInfoPath}')
	CaptureInfo = CreateCaptureInfo(CaptureName, Description)
	BedAdjustFunction = r"sed -e 's/$/\t\./'"
	# Paths
	InputPath = os.path.realpath(InputBED)
	GenomeDir = os.path.dirname(GenomeInfoPath)
	CaptureDir = os.path.join(GenomeDir, 'capture')
	OutputDir = os.path.join(CaptureDir, CaptureName)
	GenomeInfoBed = os.path.join(GenomeDir, GenomeInfo['bed'])
	CapturePath = os.path.join(GenomeDir, CaptureInfo['capture'])
	NotCapturePath = os.path.join(GenomeDir, CaptureInfo['not.capture'])
	TempPurified = os.path.join(CaptureDir, '.temp.decompressed.bed')
	ChromSizes = GenomeInfo['chrom.sizes.dict']
	# Make dirs
	try:
		os.mkdir(CaptureDir)
	except FileExistsError:
		logging.info('Captures directory already exists. Passing.')
	os.mkdir(OutputDir)
	logging.info('Directories created')
	with Open(InputPath) as Input, open(TempPurified, 'wt') as Purified:
		for Line in Input:
			SplitLine = Line.split('\t')
			ParsedLine = { 'Contig': re.sub('[^\w\.]', '_', SplitLine[0]), 'Start': int(SplitLine[1]), 'End': int(SplitLine[2]) }
			assert ParsedLine['Contig'] in ChromSizes, f'Contig "{ParsedLine["Contig"]}" is not presented in the reference: "{Line}"'
			assert ParsedLine['End'] > ParsedLine['Start'], f'Zero length interval in the BED file: "{Line}"'
			assert ParsedLine['End'] < ChromSizes[ParsedLine['Contig']], f'Interval goes out of the contig: "{Line}"'
			Purified.write(f'{ParsedLine["Contig"]}\t{ParsedLine["Start"]}\t{ParsedLine["End"]}\n')
	logging.info('BED file decompressed and purified')
	CommandFilterAndSort = ['set', '-o', 'pipefail;', 'bedtools', 'sort', '-faidx', ArmorDoubleQuotes(GenomeInfoBed), '-i', ArmorDoubleQuotes(TempPurified), '|', BedAdjustFunction, '>', ArmorDoubleQuotes(CapturePath)]
	CommandNotCapture = ['set', '-o', 'pipefail;', 'bedtools', 'subtract', '-a', ArmorDoubleQuotes(GenomeInfoBed), '-b', ArmorDoubleQuotes(CapturePath), '|', BedAdjustFunction, '>', ArmorDoubleQuotes(NotCapturePath)]
	BashSubprocess('Capture sorted and written', ' '.join(CommandFilterAndSort))
	BashSubprocess('NotCapture written', ' '.join(CommandNotCapture))
	GenomeInfo['capture'][CaptureName] = CaptureInfo
	json.dump(GenomeInfo, open(GenomeInfoPath, 'wt'), indent = 4, ensure_ascii = False)
	logging.info('Genome Info updated')
	os.remove(TempPurified)
	logging.info('Job finished')

def ListContigs(FastaPath):
	logging.info(f'{__scriptname__} Contigs {__version__}')
	FullFastaPath = os.path.realpath(FastaPath)
	Fasta = SeqIO.parse(Open(FullFastaPath), 'fasta')
	logging.info(f'FASTA opened: {FullFastaPath}')
	Result = list()
	for Contig in Fasta: Result.append(str(Contig.id))
	logging.info(f'Contigs: {json.dumps(Result)}')

def ListRS():
	logging.info(f'{__scriptname__} RestrictionSites {__version__}')
	# Config
	ConfigPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	Config = json.load(open(ConfigPath, 'rt'))
	logging.info(f'Restriction sites: {json.dumps(Config["Enzymes"])}')

def RemoveRS(Name):
	logging.info(f'{__scriptname__} RemoveRS {__version__}')
	# Config
	ConfigPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	Config = json.load(open(ConfigPath, 'rt'))
	if Name not in Config['Enzymes']:
		logging.error(f'Restriction site not found: "{Name}"')
		exit(1)
	else:
		del Config['Enzymes'][Name]
		json.dump(Config, open(ConfigPath, 'wt'))
		logging.info(f'Config saved')

def AddRS(Name, RegExp):
	logging.info(f'{__scriptname__} AddRS {__version__}')
	# Config
	ConfigPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	Config = json.load(open(ConfigPath, 'rt'))
	if Name in Config['Enzymes']:
		logging.error(f'Restriction site exists: "{Name}"')
		exit(1)
	else:
		try:
			re.compile(RegExp)
		except re.error:
			logging.error(f'RegExp is not valid: {RegExp}')
			exit(1)
		# TODO Check name?
		Config['Enzymes'][Name] = RegExp
		json.dump(Config, open(ConfigPath, 'wt'))
		logging.info(f'Config saved')

def CreateParser():
	Parser = argparse.ArgumentParser(
		formatter_class = argparse.RawDescriptionHelpFormatter,
		description = f'{__scriptname__} {__version__}: Reference Sequence and Capture Intervals Preparation for ExoClasma Suite',
		epilog = f'Bug tracker: {__bugtracker__}')
	Parser.add_argument('-v', '--version', action = 'version', version = __version__)
	Subparsers = Parser.add_subparsers(title = 'Commands', dest = 'command')
	# PrepareReference
	PrepareReferenceParser = Subparsers.add_parser('Reference', help = f'Prepare Reference Sequence. Create genomic indices for several tools, restriction sites, and GenomeInfo JSON file')
	PrepareReferenceParser.add_argument('-f', '--fasta', required = True, type = str, help = f'Raw FASTA file. May be gzipped or bzipped')
	PrepareReferenceParser.add_argument('-n', '--name', required = True, type = str, help = f'Name of reference assembly. Will be used as folder name and files prefix')
	PrepareReferenceParser.add_argument('-p', '--parent', required = True, type = str, help = f'Parent dir where reference folder will be created')
	PrepareReferenceParser.add_argument('-c', '--contigs', default = None, help = f'List of contigs to keep. Plain JSON array')
	PrepareReferenceParser.add_argument('-d', '--description', default = None, help = f'Reference description. Optional')
	PrepareReferenceParser.add_argument('-g', '--no-gatk', action = 'store_true', help = f'Do not build GATK dictionary')
	# PrepareCapture
	PrepareCaptureParser = Subparsers.add_parser('Capture', help = f'Prepare Capture BED. Filter and sort Capture BED, create NotCapture and update GenomeInfo JSON files')
	PrepareCaptureParser.add_argument('-b', '--bed', required = True, type = str, help = f'Raw BED file')
	PrepareCaptureParser.add_argument('-n', '--name', required = True, type = str, help = f'Name of capture. Will be used as folder name and files prefix')
	PrepareCaptureParser.add_argument('-g', '--genomeinfo', required = True, type = str, help = f'GenomeInfo JSON file. See "exoclasma-index Reference --help" for details')
	PrepareCaptureParser.add_argument('-d', '--description', default = None, type = str, help = f'Capture description. Optional.')
	# ListContigs
	ListContigsParser = Subparsers.add_parser('Contigs', help = f'List FASTA contigs')
	ListContigsParser.add_argument('-f', '--fasta', required = True, type = str, help = f'Raw FASTA file. May be gzipped or bzipped')
	# ListRS
	ListRSParser = Subparsers.add_parser('RestrictionSites', help = f'List restriction sites')
	# AddRS
	AddRSParser = Subparsers.add_parser('AddRS', help = f'Add restriction site')
	AddRSParser.add_argument('-n', '--name', required = True, type = str, help = f'Restriction site name')
	AddRSParser.add_argument('-r', '--regexp', required = True, type = str, help = f'Restriction site RegExp')
	# RemoveRS
	RemoveRSParser = Subparsers.add_parser('RemoveRS', help = f'Remove restriction site')
	RemoveRSParser.add_argument('-n', '--name', required = True, type = str, help = f'Restriction site name')

	return Parser

def main():
	Parser = CreateParser()
	Namespace = Parser.parse_args(sys.argv[1:])
	if Namespace.command == "Reference":
		CheckDependencies(CheckGatk = (not Namespace.no_gatk))
		FastaPath, GenomeName, ParentDir = os.path.abspath(Namespace.fasta), Namespace.name, os.path.abspath(Namespace.parent)
		ContigJSON = None if Namespace.contigs is None else str(Namespace.contigs)
		Description = None if Namespace.description is None else str(Namespace.description)
		RefseqPreparation(FastaPath = FastaPath, GenomeName = GenomeName, ParentDir = ParentDir, Description = Description, BuildGatkIndex = (not Namespace.no_gatk), ContigJSON = ContigJSON)
	elif Namespace.command == "Capture":
		CheckDependencies(CheckGatk = False)
		CaptureName, InputBED, GenomeInfoJSON = Namespace.name, os.path.abspath(Namespace.bed), os.path.abspath(Namespace.genomeinfo)
		Description = None if Namespace.description is None else str(Namespace.description)
		CapturePreparation(CaptureName = CaptureName, InputBED = InputBED, GenomeInfoJSON = GenomeInfoJSON, Description = Description)
	elif Namespace.command == "Contigs":
		FastaPath = os.path.abspath(Namespace.fasta)
		ListContigs(FastaPath = FastaPath)
	elif Namespace.command == "RestrictionSites":
		ListRS()
	elif Namespace.command == "AddRS":
		AddRS(Namespace.name, Namespace.regexp)
	elif Namespace.command == "RemoveRS":
		RemoveRS(Namespace.name)
	else: Parser.print_help()

if __name__ == '__main__': main()
