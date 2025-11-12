#!/usr/bin/perl
use strict;
use warnings;
use Cwd;
	open(my $input,  "<",  "$ARGV[0]")  or die "Can't open input: $!";
	open(my $out,  ">",  "$ARGV[0].hp")  or die "Can't open input: $!";	

###Découpage du fichier xyz en fichier pour chaque monomère.



my $i=1;
my $CAS='';
my $MW='';
my $name;
my $test_2=0;
my $numligne=0;
my $phrase_H='';
my $phrase_P='';
my $SIGMA=0;

sub check_CAS{
my ($CAS)=@_;
my($check,$sum,$i,$char);
$CAS =~ s/-//g; 
$CAS =~ s/ //g;
$check = 0+substr $CAS, -1;
$sum=0;
for($i=2;$i<=length($CAS);$i++)
{
	$char=substr($CAS,-$i,1);
	$sum+=($i-1)*$char;
}
$sum=$sum %10;
if($check==$sum)
{
	return 1;
}
else{return 0;}

}

my $CAS_found=0;
my $MW_found = 0;
my $danger = 0;
my $prudence = 0;
while (<$input>) 
{	if(/^SIGMA-ALDRICH/){
			$SIGMA=1;
	}
	if($SIGMA == 1){#CAS de Sigma
		#Recherche du numéro CAS, on ne prend que le premier
		if(/^\s*No\.-CAS\s*:\s*(\d*\-\d*\-\d*)\s*$/ && $CAS_found == 0){
			if(check_CAS($1)){
				$CAS=$1;
				$CAS_found=1;				
			}
		}elsif(/^\s*Poids moléculaire\s*:\s*([\d\,]*)\s*g\/mol\s*$/ && $MW_found == 0){
			$MW=$1;
			$MW_found=1;
		}elsif(/^\s*Nom du produit\s*:\s*(.*)\s*$/){
			$name=$1;
		}elsif(/Mention de danger/){#Recherche des phrases H
			$danger=1;	
		}elsif(/(H\d{3}( + H\d{3})?( + H\d{3})?)\s*+/ && $danger == 1){
			#print "Phrase H\t\t\t".$1."\n";
			$phrase_H .= $1.', ';
		}elsif(/Conseils de prudence/){#Recherche des phrases P	
			$prudence=1;
			$danger=0;	
		}elsif(/(P\d{3}( \+ P\d{3})?( \+ P\d{3})?)\s*+/g && $prudence == 1){
			#print "Phrase P\t\t\t".$1."\n";
			$phrase_P .= $1.', ';
		}elsif(/Autres dangers/){
			$prudence=0;
		}		
	}else{#CAS de Merck	
		if(/^\s*No\.-CAS\s*(\d*\-\d*\-\d*)\s*$/ && $CAS_found == 0){
			if(check_CAS($1)){
				$CAS=$1;
				$CAS_found=1;				
			}
		}elsif(/^\s*No\.-CAS\s*:\s*(\d*\-\d*\-\d*)\s*$/ && $CAS_found == 0){
			if(check_CAS($1)){
				$CAS=$1;
				$CAS_found=1;				
			}
		}elsif(/^\s*Nom du produit\s*:\s*(.*)\s*$/){
			$name=$1;
		}elsif(/^\s*Nom du produit\s*(.*)\s*$/){
			$name=$1;
		}elsif(/^\s*M\s*([\d\,]*)\s*g\/mol\s*$/ && $MW_found == 0){
			$MW=$1;
			$MW_found=1;
		}elsif(/^\s*Poids moléculaire\s*:\s*([\d\,]*)\s*g\/mol\s*$/ && $MW_found == 0){
			$MW=$1;
			$MW_found=1;
		}elsif(/Mentions de danger/){#Recherche des phrases H
			$danger+=1;	
		}elsif(/\s*Mention de danger\s*/){#Recherche des phrases H
			$danger+=1;	
		}elsif(/^\s*(H\d{3}\w?( + H\d{3}\w?)?( + H\d{3}\w?)?)\s*+/ && $danger == 1){
			#print "Phrase H\t\t\t".$1."\n".$_."\n";
			$phrase_H .= $1.', ';
		}elsif(/Conseils de prudence/){#Recherche des phrases P	
			$prudence+=1;
			$danger-=1;	
		}elsif(/^\s*(P\d{3}( \+ P\d{3})?( \+ P\d{3})?)\s*+/g && $prudence == 1){
			#print "Phrase P\t\t\t".$1."\n";
			$phrase_P .= $1.', ';
		}elsif(/^Etiquetage réduit/){
			$prudence=-5;
			$danger=-5;
		}	
	}
}
$phrase_P=substr($phrase_P,0, -2);
$phrase_H=substr($phrase_H,0, -2);
#print $ARGV[0];
print $name."\\newline (".$CAS.", ".$MW." g/mol) & \\includegraphics[height=24pt,valign=t]{pictos/.pdf} &  \n";
print $phrase_H.'\\newline '.$phrase_P."\\\\\n";
#print "Phrases H\t\t".$phrase_H."\n";
#print "Phrases P\t\t".$phrase_P."\n";


    my $dir = substr($ARGV[0],0, -4);
#print $dir."\n";
    opendir(DIR, $dir) or die $!;

    while (my $file = readdir(DIR)) {

        # Use a regular expression to ignore files beginning with a period
        next if ($file =~ m/^\./);
			next if ($file =~ m/\.ppm/);
	#print "$file\n";

    }

    closedir(DIR);
