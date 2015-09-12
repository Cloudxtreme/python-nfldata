#!/usr/bin/perl

use IO::Uncompress::AnyInflate qw(anyinflate $AnyInflateError) ;
use WWW::Mechanize;

=head

my $mech = WWW::Mechanize->new();
my $url = 'http://www.footballoutsiders.com';

$mech->get($url);

if ($mech->form_id('user-login-form')) 
{
  $mech->submit_form(
    form_id => 'user-login-form',
    fields      => {
      name    => 'eric.truett@gmail.com',
      pass    => 'cft0911',
    }
  );

  print $mech->title();
}

else
{
  print $mech->title();
}

$mech->get('http://www.footballoutsiders.com/store/myfiles/');
$mech->get('http://www.footballoutsiders.com/store/myfiles/76159/download?file=KUBIAK2015.zip');
$mech->save_content('kubiak.zip');

=cut

anyinflate 'kubiak.zip' => 'kubiak.xls' or die "anyinflate failed: $AnyInflateError\n";
