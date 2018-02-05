#!/usr/bin/perl
use Digest::SHA qw(hmac_sha1_hex);

print "Content-type: text/plain\n\n";

$payload = join "", <STDIN>;
open F, "../.github_secret";
$secret = <F>;
close F;
chomp $secret;

$verifyKey = $ENV{HTTP_X_HUB_SIGNATURE};
my $testKey = 'sha1='.hmac_sha1_hex($payload, $secret);
#print "id=", `id`, "secret='$secret'\n", "verifyKey='$verifyKey'\n", "testKey='$testKey'\n", "payload='$payload'\n";

if (!$verifyKey || $verifyKey ne $testKey) {
    print "Not Verified\n";
    exit 1;
} else {
    print "Verified\n";
    system "../scripts/git_pull.sh";
    exit 0;
}
