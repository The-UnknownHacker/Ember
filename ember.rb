class Ember < Formula
    desc "The Offical Ember language executable"
    homepage "https://github.com/The-UnknownHacker/Ember"
    url "https://github.com/The-UnknownHacker/Ember/releases/download/v0/ember"
    version "0.3"  # Update this with your version
    sha256 "541c41415b655693a595cb977efdde790057287f8866627f4ed3c1bcc2212f23"
  
    def install
      bin.install "ember"
    end
  
    test do
      system "#{bin}/ember", "--version"
    end
  end
  